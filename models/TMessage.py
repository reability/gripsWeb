from datetime import datetime

from models.Ticket import Ticket


class TMessage:

    def __init__(self, title: str, description: str):
        self.title = title
        self.description = description

    @staticmethod
    def init_from(ticket_model: Ticket.Model):
        return TMessage(title=ticket_model.title, description="")

    @staticmethod
    def _description_for(model: Ticket.Model):
        return "{date}\n{description}\n\n{url}".format(
            date=datetime.fromtimestamp(model.post_date).strftime("%m/%d, %H:%M:%S"),
            description=model.description,
            url=model.original_url
        )

    def to_str(self):
        return "{0}\n{1}".format(self.title, self.description)
