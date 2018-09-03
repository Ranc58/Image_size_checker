from aiohttp_utils.routing import ResourceRouter
from views import ImagesHandler, ImageHandler


def setup_routes(router: ResourceRouter) -> None:
    router.add_resource_object('/api/v1/images', ImagesHandler())
    router.add_resource_object('/api/v1/images/{pk}', ImageHandler())
