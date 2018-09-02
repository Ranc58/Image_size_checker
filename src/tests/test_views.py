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

    async def get_application(self):

        app = web.Application(router=routing.ResourceRouter())
        app['db'] = MockedDB()
        setup_routes(app.router)
        setup_middlewares(app.middlewares)
        return app


class TestImagesHandler(BaseTestCase):

    @unittest_run_loop
    async def test_post_one_image(self):
        img_url = 'http://www.test.com/img.png'
        check_result = {
            'url': img_url,
            'width': random.randint(100, 200),
            'height': random.randint(100, 200),
            'created_at': str(datetime.now())
        }
        with asynctest.patch.object(
                image_checker.ImageChecker,
                'get_info',
                side_effect=check_result):
            resp = await self.client.request(
                "POST", "api/v1/images",
                json={"url": img_url}
            )
            self.assertEqual(resp.status, 201)
            self.assertEqual(resp.body['result'], check_result)

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
            'created_at': str(datetime.now())
        } for img_url in imgs_urls]
        with asynctest.patch.object(
                image_checker.ImageChecker,
                'get_info',
                side_effect=check_results):
            resp = await self.client.request(
                "POST", "api/v1/images",
                json=[{'url': img_url} for img_url in imgs_urls]
            )
            self.assertEqual(resp.status, 201)
            self.assertEqual(resp.body['result'], check_results)




