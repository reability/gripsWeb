from aiohttp import web
import app

if __name__ == '__main__':
    app = app.init_app()

    web.run_app(app, host="0.0.0.0", port=8080)
