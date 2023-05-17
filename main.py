import requests
import os
import os.path
from urllib.parse import urlparse, urlencode
from dotenv import load_dotenv
import argparse
import telegram
from datetime import datetime


def send_telegram(bot, list_pictures):
    for file_name in list_pictures:
        with open(file_name, 'rb') as file:
            bot.send_document(chat_id=-997935206, document=file)


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
    list_pictures = []
    for picture_number, picture in enumerate(pictures):
        file_name = download_image(picture, 'images/spacex_{}'.format(picture_number))
        list_pictures.append(file_name)
    return list_pictures



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


if __name__ == "__main__":
    if not os.path.exists('images'):
        os.makedirs('images')

    if not os.path.exists('nasa'):
        os.makedirs('nasa')

    if not os.path.exists('epic'):
        os.makedirs('epic')

    parser = argparse.ArgumentParser(description='Программа скачивает NASA фотографии')
    parser.add_argument('apod_count', metavar='amountD',  type=int, help='amount of everyday pictures that needs to download in directory nasa')
    parser.add_argument('epic_count', metavar='amountE',  type=int, help='amount of epic pictures that needs to download in directory epic')
    args = parser.parse_args()
    load_dotenv()
    telebot_token = os.getenv("TELEBOT_TOKEN")
    bot = telegram.Bot(token=telebot_token)

    apod_token = os.getenv('APOD_TOKEN')
    epic_token = os.getenv("EPIC_TOKEN")
    spacex_lauch_id = os.getenv("SPACEX_LAUNCH_ID")
    list_pictures_day = fetch_nasa_day_pictures(apod_token, args.apod_count)
    list_pictures_epic = fetch_nasa_epic_pictures(epic_token, args.epic_count)
    list_pictures_spacex = fetch_spacex_last_launch(spacex_lauch_id)
    for pictures in list_pictures_day, list_pictures_epic, list_pictures_spacex:
        send_telegram(bot, pictures)

