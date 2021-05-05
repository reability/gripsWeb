from datetime import datetime


class Ticket:

    COLLECTION = "Tickets"

    class Model:

        TICKET_ID = "ticket_id"
        TITLE = "title"
        DESCRIPTION = "description"
        ORIGINAL_URL = "original_url"
        POST_DATE = "post_date"

        def __init__(self,
                     ticket_id: int,
                     title: str,
                     description: str,
                     original_ulr: str,
                     post_date: int  # Timestamp
                     ):
            self.ticket_id = ticket_id
            self.title = title
            self.description = description
            self.original_url = original_ulr
            self.post_date = post_date

        def as_dict(self) -> dict:
            return {
                self.TICKET_ID: self.ticket_id,
                self.TITLE: self.title,
                self.DESCRIPTION: self.description,
                self.ORIGINAL_URL: self.original_url,
                self.POST_DATE: self.post_date,
            }

        @staticmethod
        def from_dict(dictionary):
            try:
                _ticket_id = dictionary[Ticket.Model.TICKET_ID]
                _title = dictionary[Ticket.Model.TITLE]
                _description = dictionary[Ticket.Model.DESCRIPTION]
                _original_url = dictionary[Ticket.Model.ORIGINAL_URL]
                _post_date = dictionary[Ticket.Model.POST_DATE]

                return Ticket.Model(_ticket_id, _title, _description, _original_url, _post_date)
            except KeyError:
                print("Decoding error for {0}\n Should be {1}, {2}, {3}, {4}, {5}".format(
                    dictionary,
                    Ticket.Model.TICKET_ID,
                    Ticket.Model.TITLE,
                    Ticket.Model.DESCRIPTION,
                    Ticket.Model.POST_DATE,
                    Ticket.Model.ORIGINAL_URL
                ))
                return None

    def __init__(self, db):
        self.collection = db[Ticket.COLLECTION]

    @staticmethod
    def model(json):
        return Ticket.Model.from_dict(json)

    async def read_all_after(self, date: int):
        result = await self.collection.find({Ticket.Model.POST_DATE: {'$gte': date}})
        if result:
            return await result.to_list(length=100)
        else:
            return []

    async def read_all_(self, count: int):
        result = await self.collection.find({})
        if result:
            return result.to_list(length=count)
        else:
            return None

    async def save_if_not_exist(self, entity: Model):
        if not await self.exist(entity.ticket_id):
            return await self.save(entity)

    async def save(self, entity: Model):
        result = await self.collection.insert_one(entity.as_dict())
        return result

    async def exist(self, ticket_id: int) -> bool:
        result = await self.collection.find_one({Ticket.Model.TICKET_ID: ticket_id})
        if result:
            return True
        else:
            return False
