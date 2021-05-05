from aiohttp import web
import asyncio
import app

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    app = app.init_app(loop)

    web.run_app(app, host="0.0.0.0", port=8080)
