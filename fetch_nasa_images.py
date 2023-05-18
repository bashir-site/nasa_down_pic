import requests
import os
from dotenv import load_dotenv
import argparse
from comon_code import download_image,send_telegram


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


parser = argparse.ArgumentParser(description='Программа загрузит фото от Nasa в указаном количестве.')
parser.add_argument('--count', metavar='count', type=int, help='Количество загружаемых фото')
args = parser.parse_args()

load_dotenv()
apod_token = os.getenv('APOD_TOKEN')
telebot_token = os.getenv("TELEBOT_TOKEN")
tg_chat_id = os.getenv('TG_CHAT_ID')
list_pictures = fetch_nasa_day_pictures(apod_token, int(args.count or 5))
send_telegram(telebot_token, tg_chat_id, list_pictures)

