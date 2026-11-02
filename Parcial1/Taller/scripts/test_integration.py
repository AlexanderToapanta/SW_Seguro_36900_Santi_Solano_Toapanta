"""Taller JWT: dos APIs reales y dos BD temporales, con limpieza al terminar.
Ejecutar con product-service-fast-api/.venv/bin/python scripts/test_integration.py.
"""
import base64
import hashlib
import hmac
import json
import os
from pathlib import Path
import secrets
import socket
import subprocess
import sys
import tempfile
import time
from uuid import uuid4

from dotenv import dotenv_values
import httpx
import psycopg
from psycopg import sql

ROOT = Path(__file__).resolve().parents[1]
USERS = ROOT / 'ms-users-nestjs'
PRODUCTS = ROOT / 'product-service-fast-api'

def run(args, cwd, env):
    p=subprocess.run(args,cwd=cwd,env=env,capture_output=True,text=True,timeout=90)
    if p.returncode: raise AssertionError(f"Falló {args[0]}: {p.stdout} {p.stderr}")

def free_port():
    with socket.socket() as s:
        s.bind(('127.0.0.1',0))
        return s.getsockname()[1]

def database_admin(cfg, users=False):
    return psycopg.connect(host=cfg['DB_HOST'],port=cfg['DB_PORT'],
        user=cfg['DB_USERNAME' if users else 'DB_USER'],password=cfg['DB_PASSWORD'],
        dbname=cfg['DB_DATABASE' if users else 'DB_NAME'],autocommit=True)

def stop(process):
    if process and process.poll() is None:
        process.terminate()
        try: process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            process.kill(); process.wait(timeout=5)

def wait_api(url, process):
    for _ in range(100):
        if process.poll() is not None: raise AssertionError('La API terminó durante el arranque')
        try:
            if httpx.get(url, timeout=1, trust_env=False).status_code == 200: return
        except httpx.HTTPError: pass
        time.sleep(0.1)
    raise AssertionError('La API no respondió a tiempo')

def main():
    users_cfg=dict(dotenv_values(USERS/'.env'))
    product_cfg=dict(dotenv_values(PRODUCTS/'.env'))
    user_db='taller_users_'+uuid4().hex
    product_db='taller_products_'+uuid4().hex
    up,pp=free_port(),free_port()
    while up==pp: pp=free_port()
    uenv={**os.environ,**users_cfg,'DB_DATABASE':user_db,'PORT':str(up),'NODE_ENV':'test','JWT_SECRET':secrets.token_urlsafe(48)}
    penv={**os.environ,**product_cfg,'DB_NAME':product_db,'ENABLE_SEED':'true','USER_SERVICE_URL':f'http://127.0.0.1:{up}'}
    user_process=product_process=None
    connections=[]; created=[]
    passed=[]
    with tempfile.TemporaryDirectory(prefix='taller-jwt-') as temp:
        user_log=open(Path(temp)/'users.log','w+')
        product_log=open(Path(temp)/'products.log','w+')
        try:
            for cfg,is_user,name in [(users_cfg,True,user_db),(product_cfg,False,product_db)]:
                conn=database_admin(cfg,is_user); connections.append(conn)
                conn.execute(sql.SQL('CREATE DATABASE {}').format(sql.Identifier(name)))
                created.append((conn,name))
            run(['npm','run','build'],USERS,uenv)
            run(['node','node_modules/typeorm/cli.js','-d','dist/database/data-source.js','migration:run'],USERS,uenv)
            run(['node','dist/database/seed.js'],USERS,uenv)
            user_process=subprocess.Popen(['node','dist/main.js'],cwd=USERS,env=uenv,stdout=user_log,stderr=subprocess.STDOUT)
            wait_api(f'http://127.0.0.1:{up}/api/v1/health',user_process)
            product_process=subprocess.Popen([sys.executable,'-m','uvicorn','app.main:app','--host','127.0.0.1','--port',str(pp)],cwd=PRODUCTS,env=penv,stdout=product_log,stderr=subprocess.STDOUT)
            wait_api(f'http://127.0.0.1:{pp}/health',product_process)
            with httpx.Client(timeout=8,trust_env=False) as client:
                def request(service, method, path, token=None, data=None, expected=200):
                    base=f'http://127.0.0.1:{up}/api/v1' if service=='u' else f'http://127.0.0.1:{pp}/api/v1'
                    headers={'Authorization':f'Bearer {token}'} if token else {}
                    response=client.request(method,base+path,headers=headers,json=data)
                    assert response.status_code==expected, f'{method} {path}: esperado {expected}, recibido {response.status_code}: {response.text}'
                    return response.json() if response.content else None
                def ok(label):
                    passed.append(label); print('OK:',label,flush=True)
                def login(username):
                    return request('u','POST','/auth/login',data={'identifier':username,'password':'ClaveSegura2026!'})
                # Cinco intentos válidos/fallidos como máximo antes de la prueba 429.
                request('u','POST','/auth/login',data={'identifier':'jperez','password':'incorrecta'},expected=401)
                a=login('jperez'); o=login('amendoza@example.com'); c=login('mgomez'); multi=login('cvega')
                at,ot,ct=a['accessToken'],o['accessToken'],c['accessToken']
                assert set(multi['user']['roles'])=={'CLIENTE','OPERADOR'}
                ok('Login por nombre/correo, contraseña inválida y usuario con varios roles')
                me=request('u','GET','/auth/me',at)
                assert {'userId','username','email','roles'}<=me.keys()
                ok('Contrato /auth/me compatible con productos')
                spec=client.get(f'http://127.0.0.1:{pp}/openapi.json').json()
                for path,ops in spec['paths'].items():
                    if path=='/health': continue
                    for op in ops.values(): assert {'BearerAuth':[]} in op['security']
                user_spec=client.get(f'http://127.0.0.1:{up}/docs-json').json()
                assert {'bearer':[]} in user_spec['paths']['/api/v1/users']['get']['security']
                ok('Swagger declara Bearer en las rutas protegidas de ambos servicios')
                request('p','GET','/products/',expected=401)
                request('p','GET','/products/',token='token_inventado',expected=401)
                request('p','GET','/products/',token=at+'alterado',expected=401)
                ok('Productos rechaza token ausente, inventado o alterado')
                def signed_token(**changes):
                    now=int(time.time())
                    payload={'sub':a['user']['id'],'username':'jperez','tokenVersion':0,'typ':'access','iat':now,'exp':now+900,'iss':uenv['JWT_ISSUER'],'aud':uenv['JWT_AUDIENCE'],**changes}
                    encode=lambda obj: base64.urlsafe_b64encode(json.dumps(obj,separators=(',',':')).encode()).rstrip(b'=')
                    message=encode({'alg':'HS256','typ':'JWT'})+b'.'+encode(payload)
                    sig=base64.urlsafe_b64encode(hmac.new(uenv['JWT_SECRET'].encode(),message,hashlib.sha256).digest()).rstrip(b'=')
                    return (message+b'.'+sig).decode()
                for claims in [{'exp':int(time.time())-10},{'iss':'otro'},{'aud':'otro'},{'typ':'refresh'}]:
                    request('p','GET','/products/',token=signed_token(**claims),expected=401)
                ok('JWT expirado, emisor/audiencia incorrectos y tipo inválido: 401')
                for token in [at,ot,ct]:
                    assert len(request('p','GET','/products/',token))==5
                    assert len(request('p','GET','/categories/',token))==5
                    assert len(request('p','GET','/product-categories/',token))==10
                ok('ADMIN, OPERADOR y CLIENTE consultan los datos de ejemplo')
                data={'sku':'DEMO-INT','nombre':'Monitor de prueba','marca':'Prueba','precio_venta':'249.99','stock':10,'stock_minimo':2}
                request('p','POST','/products/',ct,data,403)
                product=request('p','POST','/products/',ot,data,201); pid=product['id']
                assert request('p','PATCH','/products/'+pid,ot,{'stock':12})['stock']==12
                request('p','PATCH','/products/'+pid,ct,{'stock':2},403)
                request('p','DELETE','/products/'+pid,ot,expected=403)
                request('p','DELETE','/products/'+pid,ct,expected=403)
                ok('Productos: operador crea/actualiza, cliente no escribe, solo ADMIN elimina')
                category_data={'codigo':'INT','nombre':'Integración'}
                for token in [ot,ct]: request('p','POST','/categories/',token,category_data,403)
                cat=request('p','POST','/categories/',at,category_data,201); cid=cat['id']
                for token in [ot,ct]:
                    request('p','PATCH','/categories/'+cid,token,{'nombre':'Prohibido'},403)
                    request('p','DELETE','/categories/'+cid,token,expected=403)
                request('p','PATCH','/categories/'+cid,at,{'nombre':'Actualizada'})
                ok('Categorías: creación, actualización y eliminación exclusivas de ADMIN')
                relation_data={'product_id':pid,'category_id':cid}
                request('p','POST','/product-categories/',ct,relation_data,403)
                rel=request('p','POST','/product-categories/',ot,relation_data,201); rid=rel['id']
                for token in [at,ot,ct]:
                    request('p','GET','/product-categories/'+rid,token)
                    request('p','GET','/product-categories/by-product/'+pid,token)
                    request('p','GET','/product-categories/by-category/'+cid,token)
                request('p','PATCH','/product-categories/'+rid,ct,{'estado':False},403)
                request('p','DELETE','/product-categories/'+rid,ct,expected=403)
                request('p','PATCH','/product-categories/'+rid,ot,{'estado':False})
                request('p','DELETE','/product-categories/'+rid,ot,expected=204)
                ok('Relaciones: consulta de los tres roles y gestión por ADMIN/OPERADOR')
                request('p','DELETE','/products/'+pid,at)
                request('p','DELETE','/categories/'+cid,at)
                request('p','GET','/products/'+pid,at,expected=404)
                ok('Eliminación lógica realizada por ADMIN')
                for payload in [{'stock':-1},{'precio_venta':'0.001'},{'nombre':None},{'is_admin':True}]:
                    existing=request('p','GET','/products/',at)[0]['id']
                    request('p','PATCH','/products/'+existing,at,payload,422)
                ok('Entradas inválidas se rechazan antes de persistir')
                roles=request('u','GET','/roles',at)['data']; opid=next(r['id'] for r in roles if r['rol']=='OPERADOR')
                uid=o['user']['id']
                request('u','DELETE',f'/user-roles/{uid}/{opid}',at,expected=204)
                request('p','GET','/products/',ot,expected=403)
                request('u','POST','/user-roles',at,{'userId':uid,'roleId':opid},201)
                request('p','GET','/products/',ot)
                ok('Retirar y reasignar rol surte efecto con el MISMO JWT')
                request('u','PATCH','/roles/'+opid,at,{'estado':False})
                request('p','GET','/products/',ot,expected=403)
                request('u','PATCH','/roles/'+opid,at,{'estado':True})
                request('u','PATCH','/users/'+uid,at,{'estado':False})
                request('p','GET','/products/',ot,expected=401)
                request('u','PATCH','/users/'+uid,at,{'estado':True})
                ok('Rol desactivado: 403; usuario desactivado: 401')
                request('u','POST','/auth/logout',ot,expected=204)
                request('p','GET','/products/',ot,expected=401)
                ok('Logout en usuarios invalida el acceso a productos')
                request('u','PATCH','/users/'+c['user']['id'],at,{'password':'OtraClaveSegura2026!'})
                request('p','GET','/products/',ct,expected=401)
                ok('Cambio de contraseña invalida el token también en productos')
                limited = False
                for _ in range(101):
                    response=client.get(f'http://127.0.0.1:{pp}/api/v1/products/',headers={'Authorization':f'Bearer {at}'})
                    if response.status_code==503:
                        limited=True
                        break
                    assert response.status_code==200
                assert limited, 'Debe respetar el límite configurado en User Service'
                ok('Límite de /auth/me conservado: productos falla cerrado con 503 al agotarlo')
                request('u','POST','/auth/login',data={'identifier':'jperez','password':'incorrecta'},expected=429)
                ok('Login conserva límite de cinco intentos por minuto')
                stop(user_process)
                request('p','GET','/products/',at,expected=503)
                request('p','POST','/products/',at,{**data,'sku':'NO-DEBE-CREARSE'},503)
                assert client.get(f'http://127.0.0.1:{pp}/health').status_code==200
                ok('Usuarios caído: productos responde 503 y su health sigue público')
                user_process=subprocess.Popen(['node','dist/main.js'],cwd=USERS,env=uenv,stdout=user_log,stderr=subprocess.STDOUT)
                wait_api(f'http://127.0.0.1:{up}/api/v1/health',user_process)
                products=request('p','GET','/products/',at)
                assert not any(p['sku']=='NO-DEBE-CREARSE' for p in products)
                ok('Recuperación de usuarios: integración vuelve a funcionar sin escrituras no autorizadas')
            print(f'\nRESULTADO: {len(passed)} escenarios de integración correctos.',flush=True)
        except Exception:
            for label,log in [('Usuarios',user_log),('Productos',product_log)]:
                log.flush(); log.seek(0); print(label+' (diagnóstico):\n'+log.read()[-5000:],file=sys.stderr)
            raise
        finally:
            stop(product_process); stop(user_process)
            user_log.close(); product_log.close()
            for conn,name in reversed(created):
                conn.execute(sql.SQL('DROP DATABASE {} WITH (FORCE)').format(sql.Identifier(name)))
            for conn in connections: conn.close()

if __name__=='__main__': main()
