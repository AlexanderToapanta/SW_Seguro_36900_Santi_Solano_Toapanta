import unittest
from uuid import uuid4
from fastapi.testclient import TestClient
from app.main import app
from app.security.dependencies import get_current_user
from app.schemas.auth import AuthenticatedUser

class ProductsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app, raise_server_exceptions=False)
        cls.client.__enter__()

    @classmethod
    def tearDownClass(cls):
        app.dependency_overrides.clear()
        cls.client.__exit__(None, None, None)

    def setUp(self):
        self.identity('ADMIN')

    def identity(self, *roles):
        app.dependency_overrides[get_current_user] = lambda: AuthenticatedUser(
            userId=uuid4(), username='test', email='test@example.com', roles=list(roles))

    def product(self):
        data = dict(sku='T'+uuid4().hex, nombre='Producto de prueba',
            precio_venta='12.50', stock=5, stock_minimo=1)
        r = self.client.post('/api/v1/products/', json=data)
        self.assertEqual(r.status_code, 201, r.text)
        return r.json()

    def category(self):
        r = self.client.post('/api/v1/categories/', json={'codigo':'T'+uuid4().hex, 'nombre':'Prueba'})
        self.assertEqual(r.status_code, 201, r.text)
        return r.json()

    def test_health(self):
        self.assertEqual(self.client.get('/health').status_code, 200)

    def test_swagger_has_bearer_for_all_business_routes(self):
        spec=self.client.get('/openapi.json').json()
        for path, operations in spec['paths'].items():
            if path == '/health': continue
            for operation in operations.values():
                self.assertIn({'BearerAuth': []}, operation['security'])

    def test_product_crud_and_duplicates(self):
        p=self.product(); url='/api/v1/products/'+p['id']
        self.assertEqual(self.client.get(url).status_code, 200)
        self.assertEqual(self.client.patch(url, json={'stock':8}).json()['stock'],8)
        self.assertEqual(self.client.post('/api/v1/products/', json={k:p[k] for k in ['sku','nombre','precio_venta','stock','stock_minimo']}).status_code,409)
        self.assertEqual(self.client.delete(url).status_code,200)
        self.assertEqual(self.client.get(url).status_code,404)

    def test_category_crud_and_duplicates(self):
        c=self.category(); url='/api/v1/categories/'+c['id']
        self.assertEqual(self.client.get(url).status_code,200)
        self.assertEqual(self.client.patch(url,json={'nombre':'Actualizado'}).json()['nombre'],'Actualizado')
        self.assertEqual(self.client.post('/api/v1/categories/',json={'codigo':c['codigo'],'nombre':'Otro'}).status_code,409)
        self.assertEqual(self.client.delete(url).status_code,200)
        self.assertEqual(self.client.get(url).status_code,404)

    def test_relation_crud_and_both_directions(self):
        p=self.product(); c=self.category(); data={'product_id':p['id'],'category_id':c['id']}
        r=self.client.post('/api/v1/product-categories/',json=data)
        self.assertEqual(r.status_code,201,r.text); rid=r.json()['id']
        self.assertEqual(self.client.post('/api/v1/product-categories/',json=data).status_code,409)
        for path in ['/api/v1/product-categories/', '/api/v1/product-categories/by-product/'+p['id'], '/api/v1/product-categories/by-category/'+c['id']]:
            self.assertIn(rid,[x['id'] for x in self.client.get(path).json()])
        url='/api/v1/product-categories/'+rid
        self.assertEqual(self.client.get(url).status_code,200)
        self.assertFalse(self.client.patch(url,json={'estado':False}).json()['estado'])
        self.assertEqual(self.client.delete(url).status_code,204)
        self.assertEqual(self.client.get(url).status_code,404)

    def test_relation_rejects_missing_parents(self):
        self.assertEqual(self.client.post('/api/v1/product-categories/',json={'product_id':str(uuid4()),'category_id':str(uuid4())}).status_code,404)

    def test_pagination_and_uuid_validation(self):
        self.assertLessEqual(len(self.client.get('/api/v1/products/?limit=2').json()),2)
        for path in ['/api/v1/products/?limit=101','/api/v1/categories/?page=0','/api/v1/products/no-uuid']:
            self.assertEqual(self.client.get(path).status_code,422)

    def test_negative_values_and_excessive_precision(self):
        for value in ['-1','0','0.001','100000000.00']:
            r=self.client.post('/api/v1/products/',json={'sku':'BAD'+uuid4().hex,'nombre':'Prueba','precio_venta':value,'stock':1,'stock_minimo':0})
            self.assertEqual(r.status_code,422,r.text)

    def test_unknown_fields_are_rejected(self):
        r=self.client.post('/api/v1/categories/',json={'codigo':'XX','nombre':'Prueba','is_admin':True})
        self.assertEqual(r.status_code,422,r.text)

    def test_patch_null_required_fields_is_validation_error(self):
        p=self.product()
        for field in ['nombre','stock','precio_venta','estado']:
            r=self.client.patch('/api/v1/products/'+p['id'],json={field:None})
            self.assertEqual(r.status_code,422,r.text)
        self.assertEqual(self.client.patch('/api/v1/products/'+p['id'],json={'descripcion':None}).status_code,200)

    def test_deleted_parent_not_exposed_through_relations(self):
        p=self.product(); c=self.category()
        rid=self.client.post('/api/v1/product-categories/',json={'product_id':p['id'],'category_id':c['id']}).json()['id']
        self.client.delete('/api/v1/products/'+p['id'])
        self.assertEqual(self.client.get('/api/v1/product-categories/'+rid).status_code,404)
        self.assertNotIn(rid,[x['id'] for x in self.client.get('/api/v1/product-categories/by-category/'+c['id']).json()])

    def test_operator_cannot_delete_product_or_manage_categories(self):
        p=self.product(); self.identity('OPERADOR')
        self.assertEqual(self.client.get('/api/v1/products/').status_code,200)
        self.assertEqual(self.client.patch('/api/v1/products/'+p['id'],json={'stock':3}).status_code,200)
        self.assertEqual(self.client.delete('/api/v1/products/'+p['id']).status_code,403)
        self.assertEqual(self.client.post('/api/v1/categories/',json={'codigo':'XX','nombre':'Prueba'}).status_code,403)

    def test_client_cannot_write(self):
        self.identity('CLIENTE')
        self.assertEqual(self.client.get('/api/v1/products/').status_code,200)
        self.assertEqual(self.client.post('/api/v1/products/',json={}).status_code,403)

    def test_missing_token(self):
        app.dependency_overrides.clear()
        self.assertEqual(self.client.get('/api/v1/products/').status_code,401)
