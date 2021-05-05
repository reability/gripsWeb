from aiohttp import web
import app

if __name__ == '__main__':
    application = app.init_app()

    web.run_app(application, host="0.0.0.0", port=8080)
