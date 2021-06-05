from datetime import datetime
import time
import requests


class BotBot:

    BASEURL = "https://api.telegram.org"
    lastUpdate = datetime.now()

    def __init__(self):

        # Токен телеграмм бота который сидит в чате и имеет там админские права
        self.token = "1638989959:AAH_bHciQUqxWv_HCSxn-0daSkkQKSI90vU"

        # Номер чата в телеграмме куда отправляются данные
        self.chatId = -1001198075642

        BotBot.lastUpdate = datetime.now()

    def send(self, message):
        # Не даем отправлять сообщения в телеграмм чаше раза в секунду
        # Для этого мы запоминаем каждый момент отправки сообшения в телеграмм
        time_delta = self.seconds_between_requests(datetime.now())
        if time_delta < 1.0:
            time.sleep(time_delta)
        BotBot.lastUpdate = datetime.now()

        # Формируем данные для запроса на апи телеграмма и отправляем запрос
        url = self._url_for()
        data = self._data_for(text=message.to_str())
        result = requests.post(url, data=data)

        # Обновляем момент последнего апдейта телеграмм канала
        #BotBot.lastUpdate = datetime.now()
        if result.status_code == 200:
            # Сообшение успешно отправлено
            print("Sended tg", end="")
            print(message)
            return True
        else:
            # Не удалось отправить сообщение
            print(result.text)
            return False

    def _url_for(self):
        # Урл описанный в документации АПИ телеграмма для отправик сообщения ботом
        return "{0}/bot{1}/sendMessage".format(BotBot.BASEURL, self.token)

    def _data_for(self, text: str) -> dict:
        # Формат данных описанная в документации АПИ телеграмма для отправик сообщения ботом
        return {'chat_id': self.chatId,
                'text': text
                }

    def seconds_between_requests(self, d):
        return abs(d.timestamp() - BotBot.lastUpdate.timestamp())
