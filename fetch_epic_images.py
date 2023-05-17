import requests
import os
from dotenv import load_dotenv
from pathlib import Path
import argparse
from main import download_image
import telegram
from datetime import datetime


if not os.path.exists('epic'):
    os.makedirs('epic')


def fetch_nasa_epic_pictures(token_epic, count=5):
    response = requests.get('https://epic.gsfc.nasa.gov/api/natural')
    response.raise_for_status()

    images = []
    for string in response.json():
        images.append(string['image'])

    list_pictures = []
    for image_number, image in enumerate(images):
        if image_number == count:
            break
        date_str = image.replace("epic_1b_", "")[0:8]
        date_obj = datetime.strptime(date_str, '%Y%m%d')
        year, month, day = date_obj.year, date_obj.strftime('%m'), date_obj.day
        params = {
            "api_key": token_epic
        }
        url = "https://api.nasa.gov/EPIC/archive/natural/{}/{}/{}/png/{}.png".format(year, month, day, image)
        file_name = download_image(url, 'epic/epic_{}'.format(image_number), params)
        list_pictures.append(file_name)
    return list_pictures


def send_telegram(bot, list_pictures):
    for file_name in list_pictures:
        with open(file_name, 'rb') as file:
            bot.send_document(chat_id=-997935206, document=file)

parser = argparse.ArgumentParser(description='Программа загрузит EPIC фото в указаном количестве.')
parser.add_argument('--count', metavar='count', type=int, help='Количество загружаемых фото')
args = parser.parse_args()

env_path = Path('.') / '.env'
load_dotenv()
epic_token = os.getenv("EPIC_TOKEN")
telebot_token = os.getenv("TELEBOT_TOKEN")
bot = telegram.Bot(token=telebot_token)

list_pictures = fetch_nasa_epic_pictures(epic_token, int(args.count or 5))
send_telegram(bot, list_pictures)


