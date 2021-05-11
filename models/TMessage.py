from datetime import datetime

from models.Ticket import Ticket


class TMessage:

    def __init__(self, title: str, description: str):
        self.title = title
        self.description = description

    @staticmethod
    def init_from(ticket_model: Ticket.Model):
        return TMessage(title=ticket_model.title, description=TMessage._description_for(ticket_model))

    @staticmethod
    def _description_for(model: Ticket.Model):
        print(model.post_date)
        print(type(model.post_date))
        return "{date}\n{description}\n\n{url}".format(
            date=datetime.fromtimestamp(int(model.post_date)).strftime("%m/%d, %H:%M:%S"),
            description=model.description,
            url=model.original_url
        )

    def to_str(self):
        return "**{0}**\n\n{1}".format(self.title, self.description)
