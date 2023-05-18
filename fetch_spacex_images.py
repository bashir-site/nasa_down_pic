import requests
import os
from dotenv import load_dotenv
import argparse
from comon_code import download_image, send_telegram


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


parser = argparse.ArgumentParser(description='Программа загрузит фото от SpaceX по указанному ID запуска.')
parser.add_argument('--id', metavar='spacex_lauch_id', help='ID запуска')
args = parser.parse_args()
load_dotenv()
spacex_lauch_id = os.getenv("SPACEX_LAUNCH_ID")
telebot_token = os.getenv("TELEBOT_TOKEN")
tg_chat_id = os.getenv('TG_CHAT_ID')

list_pictures = fetch_spacex_last_launch(str(args.id or spacex_lauch_id))
send_telegram(telebot_token, tg_chat_id, list_pictures)
