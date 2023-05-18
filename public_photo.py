import schedule
import requests
import os
import random
import telegram
from dotenv import load_dotenv


load_dotenv()
telebot_token = os.getenv("TELEBOT_TOKEN")
bot = telegram.Bot(token=telebot_token)
tg_chat_id = os.getenv('TG_CHAT_ID')

def send_photo(folder):
    for epic_picture_number, epic_picture in enumerate(epic_pictures_dirs):
        file = epic_pictures_dirs.pop(epic_picture_number)
        with open('{}/{}'.format(folder, file), 'rb') as photo:
            bot.send_document(chat_id=tg_chat_id, document=photo)


def shuffle_photo(folder):
    for epic_picture_number, epic_picture in enumerate(epic_pictures_dirs):
        file = random.shuffle(epic_picture)
        file  = file.pop(epic_picture_number)
        with open('{}/{}'.format(folder, file), 'rb') as photo:
            bot.send_document(chat_id=tg_chat_id, document=photo)


epic_pictures_dirs = os.listdir('epic/')
nasa_pictures_dirs = os.listdir('nasa/')
images_pictures_dirs = os.listdir('images/')

try:
    schedule.every(14400).seconds.do(send_photo, folder="epic")
except IndexError:
    schedule.every(14400).seconds.do(shuffle_photo, folder="epic")

while True:
    schedule.run_pending()
