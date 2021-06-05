from aiohttp import web
from motor import motor_asyncio

from middlewares import db_handler, bot_handler
from models.Ticket import Ticket
from models.TMessage import TMessage
from bot import BotBot

from functools import reduce


MONGO_HOST = "mongodb://localhost:27017"
MONGO_DB_NAME = "gripDB"

routes = web.RouteTableDef()


@routes.post('/ticket')
async def post_ticket(request) -> web.Response:
    print("\nRecivied POST on /ticket/")
    json_data = await request.post()
    model = Ticket.model(json_data)
    #print("data to read - " + json_data)
    print("parsed data - " + model)

    if model:
        ticket = Ticket(request.db)
        exist = await ticket.exist(model.ticket_id)
        if exist:
            print("\n RESULT: 201 - EXIST")
            return web.Response(text="Already here", status=201)
        else:
            result = await ticket.save(model)
            message_to_send = TMessage.init_from(model)
            if not request.tg_bot.send(message_to_send):
                print("\n RESULT: 502 - Failed to send: " + message_to_send + "\n\n")
                return web.Response(text="Failed to send message", status=502)
            print("\n RESULT: 200 - sended" + message_to_send + "\n\n")
            return web.Response(text="Success", status=200)
    else:
        web.Response(text="Decoding issue", status=501)


@routes.get('/ticket')
async def get_ticket(request) -> web.Response:
    ticket = Ticket(request.db)

    result = await ticket.read_all_(count=100)
    if result:
        print(result)
        tickets = reduce(lambda x, y: str(x)+str(y), result)
        return web.Response(text=tickets, status=200)
    else:
        return web.Response(text="Success", status=200)


async def init_app() -> web.Application:
    app = web.Application(middlewares=[db_handler, bot_handler])

    app.add_routes(routes)

    app.client = motor_asyncio.AsyncIOMotorClient(MONGO_HOST)
    app.db = app.client[MONGO_DB_NAME]

    app.tg_bot = BotBot()

    return app
