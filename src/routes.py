from aiohttp.web_app import Application
from aiohttp.web_urldispatcher import UrlDispatcher
from aiohttp_utils.routing import ResourceRouter, add_resource_context
from views import ImagesHandler, ImageHandler


def setup_routes(router: ResourceRouter):
    router.add_resource_object('/api/v1/images', ImagesHandler())
    router.add_resource_object('/api/v1/images/{pk}', ImageHandler())
