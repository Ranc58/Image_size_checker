from unittest.mock import Mock
from datetime import datetime
import random

from bson import ObjectId
from aiohttp import web
from aiohttp_utils import routing
from asynctest import asynctest
from aiohttp.test_utils import AioHTTPTestCase, unittest_run_loop

from routes import setup_routes
from middlewares import setup_middlewares
import image_checker


class MockedDB:

    async def insert_one(self, data):
        result = Mock()
        result.inserted_id = ObjectId()
        return result

    async def insert_many(self, **kwargs):
        result = [
            {'_id': ObjectId(), **kwarg} for kwarg in kwargs
        ]
        return result

    async def find_by_id(self, id, **kwargs):
        result = [
            {'_id': id, **kwargs}
        ]
        return result


class BaseTestCase(AioHTTPTestCase):
    response_fields = []

    async def get_application(self):
        app = web.Application(router=routing.ResourceRouter())
        app['db'] = MockedDB()
        setup_routes(app.router)
        setup_middlewares(app.middlewares)
        return app

    def assert_response_fieilds(self, response_json):
        if not isinstance(response_json, list):
            response_json = [response_json]
        for item in response_json:
            self.assertIsNot(item, None)
            for field in self.response_fields:
                self.assertIn(field, item)


class TestImagesHandler(BaseTestCase):
    response_fields = ['url', 'width', 'height']


    @unittest_run_loop
    async def test_post_one_image(self):
        img_url = 'http://www.test.com/img.png'
        check_result = {
            'url': img_url,
            'width': random.randint(100, 200),
            'height': random.randint(100, 200),
            'created_at': datetime.strftime(datetime.now(), "%Y.%m.%d %H:%M"),
        }
        with asynctest.patch.object(
                image_checker.ImageChecker,
                'get_info',
                return_value=check_result):
            resp = await self.client.request(
                "POST", "api/v1/images",
                json={"url": img_url}
            )
            resp_body = await resp.json()
            self.assertEqual(resp.status, 201)
            self.assert_response_fieilds(resp_body['result'])
            self.assertTrue(resp_body['id'])

    @unittest_run_loop
    async def test_post_many_images(self):
        imgs_urls = [
            'http://www.test.com/img.png',
            'http://www.test.com/img2.png',
            'http://www.test.com/img3.png',
        ]
        check_results = [{
            'url': img_url,
            'width': random.randint(100, 200),
            'height': random.randint(100, 200),
            'created_at': datetime.strftime(datetime.now(), "%Y.%m.%d %H:%M"),
        } for img_url in imgs_urls]
        with asynctest.patch.object(
                image_checker.ImageChecker,
                'get_info',
                return_value=check_results):
            resp = await self.client.request(
                "POST", "api/v1/images",
                json=[{'url': img_url} for img_url in imgs_urls]
            )
            resp_body = await resp.json()
            self.assertEqual(resp.status, 201)
            self.assert_response_fieilds(resp_body['result'])
            self.assertTrue(resp_body['id'])

