from aiohttp import web
from app import app
import config


def run_app() -> None:
    web.run_app(app, **config.app_run)


if __name__ == '__main__':
    run_app()
