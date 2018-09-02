from datetime import datetime
import os

import aiohttp
from PIL import Image


class ImageChecker:

    max_elements_for_check = 5
    images_path = os.path.join(os.getcwd(), 'images')


    @classmethod
    async def _download(cls, url):
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
    async def _get_sizes(cls, name):
        image_path = os.path.join(cls.images_path, name)
        image = Image.open(image_path)
        return image.width, image.height

    @classmethod
    async def get_info(cls, urls):
        data = []
        for url in urls[:cls.max_elements_for_check]:
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
