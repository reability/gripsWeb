
async def db_handler(app, handler):
    async def middleware(request):
        request.db = app.db
        response = await handler(request)
        return response
    return middleware


async def bot_handler(app, handler):
    async def middleware(request):
        request.tg_bot = app.tg_bot
        response = await handler(request)
        return response
    return middleware
