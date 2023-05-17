import requests
import os
import os.path
from urllib.parse import urlparse, urlencode
from dotenv import load_dotenv
from pathlib import Path
import argparse
import telegram


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


def fetch_spacex_last_launch(spacex_lauch_id):
    response = requests.get("https://api.spacexdata.com/v5/launches/{}".format(spacex_lauch_id))
    response.raise_for_status()
    pictures = response.json()['links']['flickr']['original']
    for picture_number, picture in enumerate(pictures):
        file_name = download_image(picture, 'images/spacex_{}'.format(picture_number))
        bot.send_document(chat_id=-997935206, document=open(file_name, 'rb'))


def fetch_nasa_day_pictures(count, apod_token):
    params = {
        "api_key": apod_token,
        "count": count
    }
    url = "https://api.nasa.gov/planetary/apod"
    response = requests.get(url, params)
    response.raise_for_status()
    for i in range(count):
        file_name = download_image(response.json()[i]['url'], 'nasa/nasa_apod_{}'.format(i), params)
        bot.send_document(chat_id=-997935206, document=open(file_name, 'rb'))


def fetch_nasa_epic_pictures(count,  epic_token):
    response = requests.get('https://epic.gsfc.nasa.gov/api/natural')
    response.raise_for_status()
    for i in range(count):
        epic_id = response.json()[i]['image']
        year, month, day = epic_id[8:12], epic_id[12:14], epic_id[14:16]
        params = {
            "api_key": epic_token
        }
        url = "https://api.nasa.gov/EPIC/archive/natural/{}/{}/{}/png/{}.png".format(year, month, day, epic_id)
        file_name = download_image(url, 'epic/epic_{}'.format(i), params)
        bot.send_document(chat_id=-997935206, document=open(file_name, 'rb'))


if __name__ == "__main__":
    if not os.path.exists('images'):
        os.makedirs('images')

    if not os.path.exists('nasa'):
        os.makedirs('nasa')

    if not os.path.exists('epic'):
        os.makedirs('epic')

    parser = argparse.ArgumentParser(description='Программа скачивает NASA фотографии')
    parser.add_argument('day_pic', metavar='amountD',  type=int, help='amount of everyday pictures that needs to download in directory nasa')
    parser.add_argument('epic_pic', metavar='amountE',  type=int, help='amount of epic pictures that needs to download in directory epic')
    args = parser.parse_args()
    env_path = Path('.') / '.env'
    load_dotenv()
    telebot_token = os.getenv("TELEBOT_TOKEN")
    bot = telegram.Bot(token=telebot_token)

    apod_token = os.getenv('APOD_TOKEN')
    epic_token = os.getenv("EPIC_TOKEN")
    spacex_lauch_id = os.getenv("SPACEX_LAUNCH_ID")
    fetch_nasa_day_pictures(args.day_pic, apod_token)
    fetch_nasa_epic_pictures(args.epic_pic, epic_token)
    fetch_spacex_last_launch(spacex_lauch_id)
