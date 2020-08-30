import time
import configuration as cfg
import requests
from datetime import datetime
from db_files.entity import Requests


# ---------------------------------------------------------------------------------------------- #
class Tbot:

    bot_cmds = ['/start', '/help', '/history']
    bot_name = 'Pluto'

    # --------------------------------------------------------------------------------------------
    def __init__(self, db_table):
        self.form = f'https://api.telegram.org/bot{cfg.token}/'
        self.update_id = -1
        self.table = db_table

    # --------------------------------------------------------------------------------------------
    def check_update(self):
        req = requests.get(f'{self.form}getUpdates', params={'offset': self.update_id}).json()
        if req['result']:
            self.update_id = req['result'][-1]["update_id"] + 1
        return None if req['result'] == [] else req

    # --------------------------------------------------------------------------------------------
    def check_url_head(self, url):
        return url if url.startswith('https://') or url.startswith('http://') else f"http://{url}"

    # --------------------------------------------------------------------------------------------
    def parse_msg(self, msg):
        """
            Return tuple with following information about message:
            (telegram_id, chat_id, req_date, origin_link, first_name, last_name)
        """
        telegram_id = msg['message']['from']['id']
        chat_id = msg['message']['chat']['id']
        req_date = datetime.fromtimestamp(msg['message']['date'])
        # Check that user send a text message
        try:
            origin_link = msg['message']['text']
        except KeyError:
            origin_link = -1
        first_name = msg['message']['from']['first_name']
        try:
            last_name = msg['message']['from']['last_name']
        except KeyError:
            last_name = None
        return telegram_id, chat_id, req_date, origin_link, first_name, last_name

    # --------------------------------------------------------------------------------------------
    def get_short_link(self, url):
        req = requests.post(cfg.short_link_request, data={"url": self.check_url_head(url)})
        if 200 <= req.status_code < 300:
            response = f'https://rel.ink/{req.json()["hashid"]}'
        else:
            response = "Invalid URL"
        return response

    # --------------------------------------------------------------------------------------------
    def put_msg_to_dbase(self, telegram_id, chat_id, req_date, origin_link, short_link, first_name, last_name):
        """ Add message to database"""
        req = Requests(telegram_id, chat_id, req_date, origin_link, short_link, first_name, last_name)
        self.table.add_request(req)

    # --------------------------------------------------------------------------------------------
    def bot_cmds_responses(self, cmd, chat_id, first_name, telegram_id):
        if cmd == '/start':
            response = f"Hello, {first_name}!\nI'm bot {self.bot_name}.\n\nYou can send me a link and i'll " \
                       f"make a short version of it for you. \nYou are also welcome to use the command /history " \
                       f"and i'll show you your last 10 requests. Type /help to see info again"
        elif cmd == '/history':
            history = [f"{num :<2})  {value.req_date.strftime('%d.%m.%Y %H:%M:%S')} | {value.short_link :<60}"
                        for num, value in enumerate(self.table.show_history(telegram_id), start=1)]
            response = '\n'.join(h for h in history)

            # Empty history case
            if response == '':
                response = "You didn't send any requests"
        elif cmd == '/help':
            response = "1) Send a link to get short version\n2) Call /history to see last 10 requests"
        data = {'chat_id': chat_id, 'text': response}
        requests.post(f"{self.form}sendMessage", data=data)

    # --------------------------------------------------------------------------------------------
    def send_msg(self, chat_id, origin_link, short_link):
        if short_link == "Invalid URL":
            text = f"<{origin_link}> invalid URL"
        else:
            text = f"Short link <{short_link}>"
        data = {'chat_id': chat_id, 'text': text}
        requests.post(f"{self.form}sendMessage", data=data)

    # --------------------------------------------------------------------------------------------
    def loop(self, timeout=1.0):
        while True:
            time.sleep(timeout)
            if msgs := self.check_update():
                for msg in msgs['result']:
                    telegram_id, chat_id, req_date, origin_link, first_name, last_name = self.parse_msg(msg)
                    # Not a text message case
                    if origin_link == -1:
                        data = {'chat_id': chat_id, 'text': "Please send a text URL"}
                        requests.post(f"{self.form}sendMessage", data=data)
                        continue
                    elif origin_link in self.bot_cmds:
                        self.bot_cmds_responses(origin_link, chat_id, first_name, telegram_id)
                    else:
                        short_link = self.get_short_link(origin_link)
                        self.put_msg_to_dbase(telegram_id, chat_id, req_date, origin_link, short_link,
                                              first_name, last_name)
                        self.send_msg(chat_id, origin_link, short_link)


# --------------------------------------------------------------------------------------------
if __name__ == '__main__':

    tbot = Tbot()
    tbot.loop(0.5)

