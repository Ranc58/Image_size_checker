from abc import ABC

import aiohttp
from aiohttp.web import Request
from aiohttp_utils import Response
from image_checker import ImageChecker

class BaseAPIHandler(ABC):
    pass


class ImagesHandler(BaseAPIHandler):

    async def post(self, request: Request) -> Response:
        pass


class ImageHandler(BaseAPIHandler):

    async def get(self, request: Request) -> Response:
        pass

