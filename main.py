from app import app
import config


def run_app():
    app.run(**config.app_run)


if __name__ == '__main__':
    run_app()
