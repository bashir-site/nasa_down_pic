import requests
import os
from dotenv import load_dotenv
from pathlib import Path
import argparse
from main import download_image
import telegram


if not os.path.exists('nasa'):
    os.makedirs('nasa')


def fetch_nasa_day_pictures(apod_token, count):
    params = {
        "api_key": apod_token,
        "count": count
    }
    url = "https://api.nasa.gov/planetary/apod"
    response = requests.get(url, params)
    response.raise_for_status()
    list_pictures = []
    for string_number, string in enumerate(response.json()):
        file_name = download_image(string['url'], 'nasa/nasa_apod_{}'.format(string_number), params)
        list_pictures.append(file_name)
    return list_pictures


def send_telegram(bot, list_pictures):
    for file_name in list_pictures:
        with open(file_name, 'rb') as file:
            bot.send_document(chat_id=-997935206, document=file)


parser = argparse.ArgumentParser(description='Программа загрузит фото от Nasa в указаном количестве.')
parser.add_argument('--count', metavar='count', type=int, help='Количество загружаемых фото')
args = parser.parse_args()

env_path = Path('.') / '.env'
load_dotenv()
apod_token = os.getenv('APOD_TOKEN')
telebot_token = os.getenv("TELEBOT_TOKEN")
bot = telegram.Bot(token=telebot_token)
list_pictures = fetch_nasa_day_pictures(apod_token, int(args.count or 5))
send_telegram(bot, list_pictures)

