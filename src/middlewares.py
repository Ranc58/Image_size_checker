from aiohttp.web_app import Application
from aiohttp_utils.negotiation import negotiation_middleware


def setup_middlewares(middlewares: Application.middlewares) -> None:
    middlewares.append(negotiation_middleware())
