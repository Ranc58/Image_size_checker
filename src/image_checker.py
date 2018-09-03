import os
from datetime import datetime
from typing import List, Dict, Tuple

import aiohttp
from PIL import Image
from settings import config


class ImageChecker:

    max_elements_for_check = config['app'].get('max_elems_for_check', 5)
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
                name = f"{datetime.now():%Y.%m.%d %H:%M}.png"
                image_path = os.path.join(cls.images_path, name)
                with open(image_path, "wb") as f:
                    f.write(data)
                return name

    @classmethod
    async def _get_sizes(cls, name: str) -> Tuple[int, int]:
        image_path = os.path.join(cls.images_path, name)
        image = Image.open(image_path)
        return image.width, image.height

    @classmethod
    def _prepare_data(cls, urls: List[Dict[str, str]]) -> List[str]:
        if len(urls) > 1:
            urls_list = [k['url'] for k in urls]
            urls_filtered = list(set(urls_list))
        else:
            urls_filtered = [urls[0].get('url')]
        return urls_filtered[:cls.max_elements_for_check]

    @classmethod
    async def get_info(cls,
                       urls: List[Dict]
                       ) -> List[Dict]:
        data: List[Dict] = []
        prepared_urls = cls._prepare_data(urls)
        for url in prepared_urls:
            name = await cls._download(url)
            width, height = await cls._get_sizes(name)
            data.append({
                'url': url,
                'width': width,
                'height': height,
                'created_at': f"{datetime.now():%Y.%m.%d %H:%M}"
            })
            os.remove(os.path.join(cls.images_path, name))
        return data
