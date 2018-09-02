import asyncio

from aiohttp import web
from aiohttp_utils import routing
from routes import setup_routes
from middlewares import setup_middlewares
from init_db import setup_db


def setup_app():
    loop = asyncio.get_event_loop()
    app = web.Application(router=routing.ResourceRouter())
    db = loop.run_until_complete(setup_db())
    app['db'] = db
    setup_routes(app.router)
    setup_middlewares(app.middlewares)
    return app
# loop = asyncio.get_event_loop()
# app = web.Application(router=routing.ResourceRouter())
# db = loop.run_until_complete(setup_db())
# app['db'] = db
#
# setup_routes(app.router)
# setup_middlewares(app.middlewares)

web.run_app(setup_app())
