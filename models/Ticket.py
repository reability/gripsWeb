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
                try:
                    _ticket_id = dictionary[Ticket.Model.TICKET_ID]
                except:
                    print("Decoding ticket issue")
                    return None
                try:
                    _title = dictionary[Ticket.Model.TITLE]
                except:
                    print("Decoding title issue")
                    return None
                try:
                    _description = dictionary[Ticket.Model.DESCRIPTION]
                except:
                    print("Decoding description issue")
                    return None
                try:
                    _original_url = dictionary[Ticket.Model.ORIGINAL_URL]
                except:
                    print("Decoding url issue")
                    return None
                try:
                    _post_date = dictionary[Ticket.Model.POST_DATE]
                    int_post_date = try_to_read(_post_date)
                    if int_post_date:
                        _post_date = int_post_date
                    else:
                        _post_date = 0
                except:
                    print("Decoding date issue")
                    return None

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
        self.db = db

    @staticmethod
    def model(json):
        return Ticket.Model.from_dict(json)

    async def read_all_after(self, date: int):
        col = self.db[self.COLLECTION]
        result = await col.find({Ticket.Model.POST_DATE: {'$gte': date}})
        if result:
            return await result.to_list(length=100)
        else:
            return []

    async def read_all_(self, count: int):
        col = self.db[self.COLLECTION]
        result = col.find({})
        if result:
            return result.to_list(length=count)
        else:
            return None

    async def save_if_not_exist(self, entity: Model):
        if not await self.exist(entity.ticket_id):
            return await self.save(entity)

    async def save(self, entity: Model):
        col = self.db[self.COLLECTION]
        result = col.insert_one(entity.as_dict())
        return result

    async def exist(self, ticket_id: int) -> bool:
        col = self.db[self.COLLECTION]
        result = await col.find_one({Ticket.Model.TICKET_ID: ticket_id})
        if result:
            return True
        else:
            return False

# MARK: - Helpers

def try_to_read(date: str):
    date_list = date.split()

    month_number = None
    day_number = None

    day_number = int(date_list[0])
    month_str = date_list[1]
    if "янв" in month_str:
        month_number = 1
    elif "фев" in month_str:
        month_number = 2
    elif "мар" in month_str:
        month_number = 3
    elif "апр" in month_str:
        month_number = 4
    elif "ма" in month_str:
        month_number = 5
    elif "июн" in month_str:
        month_number = 6
    elif "июл" in month_str:
        month_number = 7
    elif "авгу" in month_str:
        month_number = 8
    elif "сен" in month_str:
        month_number = 9
    elif "окт" in month_str:
        month_number = 10
    elif "ноя" in month_str:
        month_number = 11
    elif "дек" in month_str:
        month_number = 12

    if day_number is None or month_number is None:
        return None

    now = datetime.now()

    datedate = datetime(now.year, month_number, day_number)
    return int(datedate.timestamp())