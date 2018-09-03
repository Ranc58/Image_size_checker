import os
from datetime import datetime
from unittest.mock import patch

from PIL import Image
import asynctest
import pytest

from asynctest import TestCase

from src.image_checker import ImageChecker


class TestImageChecker(TestCase):

    @pytest.fixture(autouse=True)
    def setup(self, tmpdir):
        self.tmpdir = tmpdir

    def tearDown(self):
        self.tmpdir.remove()

    @asynctest.patch('aiohttp.ClientSession.get')
    async def test_download(self, mock_get):
        read_mock = asynctest.CoroutineMock(side_effect=[
            b'/9j/4AAQSkZJRgABAQEAYABgAAD/2wBDAA'
        ])
        mock_get.return_value.__aenter__.return_value.read = read_mock
        with patch.object(ImageChecker, 'images_path', str(self.tmpdir)):
            response = await ImageChecker._download('http://www.test.com/test.jpg')
            name = f"{datetime.now():%Y.%m.%d %H:%M}.png"
            self.assertEqual(response, name)
            self.assertTrue(os.path.exists(os.path.join(str(self.tmpdir), name)))

    async def test_get_sizes(self):
        main_path = self.tmpdir.mkdir("sub")
        with patch.object(ImageChecker, 'images_path', str(main_path)):
            name = 'test.png'
            path = str(main_path.join(name))
            img = Image.new('RGB', (60, 30), color='red')
            img.save(path)
            width, height = await ImageChecker._get_sizes(name)
            self.assertEqual((width, height), (60, 30))

    @asynctest.patch.object(ImageChecker, '_download', return_value='test.jpg')
    @asynctest.patch.object(ImageChecker, '_get_sizes', return_value=(30, 60))
    @asynctest.patch('os.remove')
    async def test_get_info(self, mocked_download, mocked_sizes, mocked_remove):
        urls = [
            {'url': 'http://www.test.com/test1.jpg'},
            {'url': 'http://www.test.com/test2.jpg'},
            {'url': 'http://www.test.com/test2.jpg'},
            {'url': 'http://www.test.com/test2.jpg'},
            {'url': 'http://www.test.com/test5.jpg'},
            {'url': 'http://www.test.com/test6.jpg'},
            {'url': 'http://www.test.com/test6.jpg'},
            {'url': 'http://www.test.com/test7.jpg'},
            {'url': 'http://www.test.com/test6.jpg'},
        ]
        expected_info_for_one_url = {
            'url': 'http://www.test.com/test1.jpg',
            'width': 30,
            'height': 60,
            'created_at': f"{datetime.now():%Y.%m.%d %H:%M}",
        }
        response = await ImageChecker.get_info(urls)
        self.assertEqual(len(response), 5)
        self.assertTrue(expected_info_for_one_url in response)

    def test_prepare_data(self):
        urls = [
            {'url': 'http://www.test.com/test1.jpg'},
            {'url': 'http://www.test.com/test2.jpg'},
            {'url': 'http://www.test.com/test2.jpg'},
            {'url': 'http://www.test.com/test2.jpg'},
            {'url': 'http://www.test.com/test5.jpg'},
            {'url': 'http://www.test.com/test6.jpg'},
            {'url': 'http://www.test.com/test6.jpg'},
            {'url': 'http://www.test.com/test7.jpg'},
            {'url': 'http://www.test.com/test6.jpg'},
        ]
        urls_list = list(set([v['url'] for v in urls]))
        expected_result = urls_list[:5]
        ImageChecker.max_elements_for_check = 5
        result = ImageChecker._prepare_data(urls)
        self.assertEqual(result, expected_result)
