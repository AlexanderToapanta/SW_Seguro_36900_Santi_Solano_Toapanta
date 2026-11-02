**Taller JWT: usuarios y productos**  
El taller integra dos APIs: NestJS autentica usuarios y administra sus roles; FastAPI gestiona productos, categorías y sus relaciones. Productos envía el token recibido a `GET /api/v1/auth/me` de usuarios y aplica los permisos usando los roles actuales. No comparte el secreto JWT ni la base de usuarios.  
Swagger permite demostrar y probar ambas APIs.  
**Arrancar en cuatro terminales visibles**  
Ejecutar en este orden. Dejar cada terminal abierta. Esperar que cada base esté lista antes de iniciar su API.  
**Terminal 1 — base de usuarios (5432):**  
```  
cd /home/jeancarlo/Desktop/U/seven/DSS/U1/Actividad1_SW_Seguro_36900/Parcial1/Taller/ms-users-nestjs  
 docker compose up postgres  
   
```  
**Terminal 2 — API de usuarios (3001):**  
```  
cd /home/jeancarlo/Desktop/U/seven/DSS/U1/Actividad1_SW_Seguro_36900/Parcial1/Taller/ms-users-nestjs  
 npm run start:dev  
   
```  
**Terminal 3 — base de productos (5433):**  
```  
cd /home/jeancarlo/Desktop/U/seven/DSS/U1/Actividad1_SW_Seguro_36900/Parcial1/Taller/product-service-fast-api  
 docker compose -f docker-compose.product-db.yml up product-postgres  
   
```  
**Terminal 4 — API de productos (8000):**  
```  
cd /home/jeancarlo/Desktop/U/seven/DSS/U1/Actividad1_SW_Seguro_36900/Parcial1/Taller/product-service-fast-api  
 source .venv/bin/activate  
 uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload  
   
```  
Abrir [Swagger de usuarios y](http://localhost:3001/docs "http://localhost:3001/docs") [Swagger de productos.](http://127.0.0.1:8000/docs "http://127.0.0.1:8000/docs")  
Para detener: `Ctrl+C` primero en las terminales de las APIs y luego en las bases. Los volúmenes conservan los datos. No usar `down -v`, porque elimina las bases.  
**Demostración breve**  
1. En productos, ejecutar `GET /health`: responde 200. Comprueba que esa API atiende; no certifica por sí solo la conexión con usuarios.  
2. Sin autorizar, ejecutar `GET /api/v1/products/`: responde 401 porque se exige un token.  
3. En usuarios, ejecutar `POST /api/v1/auth/login` con:  
```  
{"identifier":"jperez","password":"ClaveSegura2026!"}  
   
```  
1. Copiar únicamente el valor de `accessToken`. En **Authorize** de productos pegar ese valor, sin comillas y sin escribir `Bearer` delante. Swagger añadirá `Authorization: Bearer <token>` a las peticiones. Autorizar en una página no autoriza automáticamente la otra.  
2. Repetir el GET de productos: responde 200. Probar crear un producto con un SKU nuevo; responde 201. Se puede editar y eliminar con ese administrador.  
3. Iniciar sesión como `mgomez` con la misma clave de ejemplo. Reemplazar el token en productos: puede consultar (200), pero crear un producto devuelve 403. Esto demuestra autorización por roles.  
4. Para demostrar revocación, autorizar también usuarios con ese mismo token y ejecutar `POST /api/v1/auth/logout`. Al volver a consultar productos con el token anterior, responde 401.  
Las cuentas de ejemplo se destinan al laboratorio local. `amendoza` es OPERADOR; `jperez` ADMIN; `mgomez` CLIENTE. Si cambias una contraseña, usa la nueva en la demostración.  
  
|  |  |  |  |  
| - | - | - | - |  
| **Operación** |  **ADMIN** |  **OPERADOR** |  **CLIENTE** |  
| Consultar productos, categorías y relaciones |  Sí |  Sí |  Sí |  
| Crear/editar productos |  Sí |  Sí |  No |  
| Eliminar productos |  Sí |  No |  No |  
| Crear/editar/eliminar categorías |  Sí |  No |  No |  
| Crear/editar/eliminar relaciones |  Sí |  Sí |  No |  
  
   
Los eliminados se ocultan mediante borrado lógico. Un rol o usuario desactivado deja de autorizar peticiones aunque se conserve un token anterior. Logout y cambio de contraseña invalidan tokens anteriores.  
Si usuarios está caído, productos rechaza las operaciones protegidas con 503. También devuelve 503 cuando usuarios alcanza su límite de peticiones: se conserva el límite original de 100/minuto en `/auth/me`. Cada operación protegida de productos consulta usuarios, por lo que el límite puede acumularse desde una misma IP. Espera a que venza la ventana (hasta aproximadamente un minuto) y vuelve a probar.  
**Repetir las pruebas**  
Mantener ambas bases encendidas. No hace falta iniciar manualmente las APIs para estas pruebas: los runners inician y limpian sus servidores y bases temporales. El usuario de PostgreSQL del laboratorio necesita permiso para crear bases (los contenedores locales ya lo tienen).  
Desde `ms-users-nestjs`:  
```  
npm test  
 npm run lint  
 npm run test:e2e  
   
```  
Desde `product-service-fast-api`:  
```  
.venv/bin/python scripts/test_local.py  
 .venv/bin/python ../scripts/test_integration.py  
   
```  
Resultados y alcance: [Verificacion.md.](Verificacion.md "Verificacion.md")  
**Preparación en otra computadora**  
Requisitos: Docker con Compose, Node.js 24 y Python con soporte venv (validado aquí con Python 3.14). Los `.env`, dependencias y datos Docker no se suben a Git.  
En usuarios:  
```  
cp example.env.dist .env  
 # Editar .env: clave de PostgreSQL y JWT_SECRET largos y propios.  
 npm ci  
 docker compose up -d --wait  
 npm run migration:run  
 npm run seed  
   
```  
En una base nueva se ejecutan las migraciones. `migration:baseline` es solo para reconocer un esquema existente después de comprobar que coincide; no es el inicio normal de una base vacía.  
En productos:  
```  
cp example.env.dist .env  
 # Editar .env: contraseña propia y USER_SERVICE_URL=http://127.0.0.1:3001  
 python3 -m venv .venv  
 source .venv/bin/activate  
 python -m pip install -r requirements.txt  
 docker compose -f docker-compose.product-db.yml up -d --wait  
 python -m app.db.init_db  
 python -m app.db.seed  
   
```  
Si Ubuntu no tiene soporte venv, instalar el paquete `python3-venv` de la versión de Python utilizada. Mantener `ENABLE_SEED=false`; el seed se ejecuta manualmente una vez. Volver a ejecutarlo puede restablecer datos de ejemplo. Productos usa creación inicial de tablas conforme al taller; no incorpora un sistema de migraciones de producción.  
Después detener las bases con `docker compose stop` y `docker compose -f docker-compose.product-db.yml stop`, respectivamente, para seguir el arranque visible de cuatro terminales.  
