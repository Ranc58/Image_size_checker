from abc import ABC

import aiohttp
from aiohttp.web import Request
from aiohttp_utils import Response
from image_checker import ImageChecker


import forms
import serializers
from marshmallow import ValidationError


class BaseAPIHandler:

    def return_error(self, errors):
        return Response(status=400, data={'status': 'error', 'errors': errors})


class ImagesHandler(BaseAPIHandler):

    async def post(self, request: Request) -> Response:
        data = await request.json()
        try:
            forms.ImageSchema(many=True).load(data)
        except ValidationError as err:
            return self.return_error(err.messages)
        if not isinstance(data, list):
            data = [data]
        imgs_info = await ImageChecker.get_info(
            data
        )
        result = await request.app['db'].insert_one(imgs_info)
        serialized_data = serializers.ImageSerializer.to_api_object(imgs_info)
        return Response(status=201, data={"id": str(result.inserted_id), "result": serialized_data})


class ImageHandler(BaseAPIHandler):

    async def get(self, request: Request) -> Response:
        pk = request.match_info.get('pk')
        if not pk:
            raise aiohttp.web.HTTPNotFound()
        result = await request.app['db'].find_by_id(pk)
        if result:
            result.pop('_id')
        return Response(status=200, data={"id": pk, 'result': result})

