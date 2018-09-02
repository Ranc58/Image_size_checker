import os
from datetime import datetime


import aiohttp
from PIL import Image


class ImageChecker:

    max_elements_for_check = 5
    images_path = os.path.join(os.getcwd(), 'images')

    @classmethod
    async def _download(cls, url: str) -> str:
        async with aiohttp.ClientSession(
                connector=aiohttp.TCPConnector(
                    verify_ssl=False,
                    limit=1,
                ),
        ) as session:
            async with session.get(url) as resp:
                data = await resp.read()
                name = '{}.png'.format(datetime.strftime(datetime.now(), "%Y.%m.%d %H:%M"))
                image_path = os.path.join(cls.images_path, name)
                with open(image_path, "wb") as f:
                    f.write(data)
                return name

    @classmethod
    async def _get_sizes(cls, name: str) -> tuple:
        image_path = os.path.join(cls.images_path, name)
        image = Image.open(image_path)
        return image.width, image.height

    @classmethod
    def _prepare_data(cls, urls: dict or list, max_request_url=None) -> list:
        sliced_list = cls.max_elements_for_check
        if max_request_url:
            sliced_list = max_request_url
        if len(urls) > 1:
            urls_list = [k['url'] for k in urls]
            urls_filtered = list(set(urls_list))
        else:
            urls_filtered = [urls[0].get('url')]
        return urls_filtered[:sliced_list]

    @classmethod
    async def get_info(cls, urls: list) -> list:
        data = []
        prepared_urls = cls._prepare_data(urls)
        for url in prepared_urls:
            name = await cls._download(url)
            width, height = await cls._get_sizes(name)
            data.append({
                'url': url,
                'width': width,
                'height': height,
                'created_at': datetime.strftime(datetime.now(), "%Y.%m.%d %H:%M")
            })
            os.remove(os.path.join(cls.images_path, name))
        return data
