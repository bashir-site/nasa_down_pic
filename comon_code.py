import telegram
from urllib.parse import urlparse, urlencode
import requests
import os


def get_file_extension(link):
    file = urlparse(link)
    extension = os.path.splitext(file.path)
    return extension[1]


def download_image(link, name, payload={}):
    payload = urlencode(payload)
    response = requests.get(link, params=payload)
    response.raise_for_status()
    url = get_file_extension(link)
    file_name = '{}{}'.format(name, url)
    with open(file_name, 'wb') as file:
        file.write(response.content)
    return file_name


def send_photo_tg_bot(telebot_token, tg_chat_id, file_name):
    bot = telegram.Bot(token=telebot_token)
    with open(file_name, 'rb') as file:
        bot.send_document(chat_id=tg_chat_id, document=file)
