#!/usr/bin/env python
import telegram
import logging
import time
import os
from flask import Flask, request
from settings import HOST, PORT, TOKEN

app = Flask(__name__)
bot = telegram.Bot(token=TOKEN)


@app.route('/')
def hello():
    return 'Ngrok was successfully set'


@app.route('/' + TOKEN, methods=['POST'])
def webhook():
    from telegram_bot import TelegramBot
    telegram_bot = TelegramBot(request)
    telegram_bot.parse_commands()
    return 'Ok'


def set_webhook():
    time.sleep(2)
    if bot.set_webhook(url=HOST + TOKEN):
        logging.info('WebHook was set')
    else:
        logging.info('WebHook wasnt set')


if __name__ == '__main__':
    logging.basicConfig(filename=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs/bot.log'),
                        level=logging.DEBUG,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    set_webhook()
    app.run(host='0.0.0.0',
            port=PORT,
            debug=True)
