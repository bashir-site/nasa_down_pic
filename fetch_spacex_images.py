import requests
import os
from dotenv import load_dotenv
from pathlib import Path
import argparse
from main import download_image
import telegram


if not os.path.exists('images'):
    os.makedirs('images')


def fetch_spacex_last_launch(spacex_lauch_id):
    response = requests.get("https://api.spacexdata.com/v5/launches/{}".format(spacex_lauch_id))
    response.raise_for_status()
    pictures = response.json()['links']['flickr']['original']
    list_pictures = []
    for picture_number, picture in enumerate(pictures):
        file_name = download_image(picture, 'images/spacex_{}'.format(picture_number))
        list_pictures.append(file_name)
    return list_pictures


def send_telegram(bot, list_pictures):
    for file_name in list_pictures:
        with open(file_name, 'rb') as file:
            bot.send_document(chat_id=-997935206, document=file)


parser = argparse.ArgumentParser(description='Программа загрузит фото от SpaceX по указанному ID запуска.')
parser.add_argument('--id', metavar='amountD', help='ID запуска')
args = parser.parse_args()
env_path = Path('.') / '.env'
load_dotenv()
spacex_lauch_id = os.getenv("SPACEX_LAUNCH_ID")
telebot_token = os.getenv("TELEBOT_TOKEN")
bot = telegram.Bot(token=telebot_token)

list_pictures = fetch_spacex_last_launch(str(args.id or spacex_lauch_id))
send_telegram(bot, list_pictures)

