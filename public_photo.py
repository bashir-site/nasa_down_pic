import schedule
import requests
import os
import random
import telegram
from dotenv import load_dotenv
from pathlib import Path

env_path = Path('.') / '.env'
load_dotenv()
telebot_token = os.getenv("TELEBOT_TOKEN")
bot = telegram.Bot(token=telebot_token)


def send_photo():
    for i in range(1):
        file = epic.pop(i)
        with open('epic/{}'.format(file), 'rb', encoding='utf-8') as send:
            bot.send_document(chat_id=-997935206, document=send)


def shuffle_photo():
    for i in range(4):
        file = random.shuffle(epic)
        file  = file.pop(i)
        with open('epic/{}'.format(file), 'rb', encoding='utf-8') as send:
            bot.send_document(chat_id=-997935206, document=send)


epic = os.listdir('epic/')
nasa = os.listdir('nasa/')
images = os.listdir('images/')

try:
    schedule.every(14400).seconds.do(send_photo)
except:
    schedule.every(14400).seconds.do(shuffle_photo)

while True:
    schedule.run_pending()
