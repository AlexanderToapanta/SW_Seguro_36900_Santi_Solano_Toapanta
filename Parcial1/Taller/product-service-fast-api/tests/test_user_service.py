import unittest
from uuid import uuid4
import httpx
from fastapi import HTTPException
from app.clients.user_service import validate_user_token

class UserServiceClientTests(unittest.IsolatedAsyncioTestCase):
    async def check_response(self, response, expected):
        async with httpx.AsyncClient(base_url='http://users',transport=httpx.MockTransport(lambda _:response)) as client:
            with self.assertRaises(HTTPException) as error:
                await validate_user_token(client,'test-token')
            self.assertEqual(error.exception.status_code,expected)

    async def test_remote_status_mapping(self):
        for status,expected in [(401,401),(403,403),(429,503),(500,503),(302,502),(404,502)]:
            with self.subTest(status=status): await self.check_response(httpx.Response(status),expected)

    async def test_malformed_json_rejected(self):
        await self.check_response(httpx.Response(200,text='not json'),502)

    async def test_invalid_user_contract_rejected(self):
        await self.check_response(httpx.Response(200,json={'roles':['ADMIN']}),502)

    async def test_timeout_fails_closed(self):
        def handler(_): raise httpx.ReadTimeout('timeout')
        async with httpx.AsyncClient(base_url='http://users',transport=httpx.MockTransport(handler)) as client:
            with self.assertRaises(HTTPException) as error: await validate_user_token(client,'test')
            self.assertEqual(error.exception.status_code,503)

    async def test_connection_failure_fails_closed(self):
        def handler(_): raise httpx.ConnectError('offline')
        async with httpx.AsyncClient(base_url='http://users',transport=httpx.MockTransport(handler)) as client:
            with self.assertRaises(HTTPException) as error: await validate_user_token(client,'test')
            self.assertEqual(error.exception.status_code,503)

    async def test_roles_and_request_id(self):
        def handler(request):
            self.assertEqual(request.headers['Authorization'],'Bearer test')
            self.assertEqual(request.headers['X-Request-Id'],'prueba-123')
            return httpx.Response(200,json={'userId':str(uuid4()),'username':'test','email':'test@example.com','roles':[' operador ','OPERADOR']})
        async with httpx.AsyncClient(base_url='http://users',transport=httpx.MockTransport(handler)) as client:
            user=await validate_user_token(client,'test','prueba-123')
            self.assertEqual(user.roles,['OPERADOR'])
