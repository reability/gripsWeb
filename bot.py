import requests


class BotBot:

    BASEURL = "https://api.telegram.org"

    def __init__(self):
        self.token = "1638989959:AAH_bHciQUqxWv_HCSxn-0daSkkQKSI90vU"
        self.chatId = -1001198075642

    def send(self, message):
        url = self._url_for()
        data = self._data_for(text=message.to_str())
        result = requests.post(url, data=data)
        if result.status_code == 200:
            print("sended", end="")
            print(message)
            return True
        else:
            print(result.text)
            return False

    def _url_for(self):
        return "{0}/bot{1}/sendMessage".format(BotBot.BASEURL, self.token)

    def _data_for(self, text: str) -> dict:
        return {'chat_id': self.chatId,
                'text': text
                }
