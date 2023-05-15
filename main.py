import requests
import os
import os.path
from urllib.parse import urlparse
from dotenv import load_dotenv
from pathlib import Path
import argparse
from tele_bot import bot


def get_file_extension(link):
    file = urlparse(link)
    extension = os.path.splitext(file.path)
    return extension[1]


def download_image(link, save_name):
    response = requests.get(link)
    response.raise_for_status()
    url = get_file_extension(link)
    file_name = '{}{}'.format(save_name, url)
    with open(file_name, 'wb') as file:
        file.write(response.content)


def fetch_spacex_last_launch(id):
    url = "https://api.spacexdata.com/v5/launches/{}".format(id)
    response = requests.get(url)
    response.raise_for_status()
    pictures = response.json()['links']['flickr']['original']
    for picture_number, picture in enumerate(pictures):
        file_name = download_image(picture, 'images/spacex_{}'.format(picture_number))
        bot.send_document(chat_id=-997935206, document=open(file_name, 'rb'))


def fetch_nasa_day_pictures(count, token_apod):
    payload = {
        "count": count,
        "api_key": token_apod
    }
    url = "https://api.nasa.gov/planetary/apod"
    response = requests.get(url, params=payload)
    response.raise_for_status()
    for i in range(count):
        file_name = download_image(response.json()[i]['url'], 'nasa/nasa_apod_{}'.format(i))
        bot.send_document(chat_id=-997935206, document=open(file_name, 'rb'))


def fetch_nasa_epic_pictures(count, token_epic):
    response = requests.get('https://epic.gsfc.nasa.gov/api/natural')
    response.raise_for_status()
    for i in range(count):
        epic_id = response.json()[i]['image']
        year = epic_id[8:12]
        month = epic_id[12:14]
        day = epic_id[14:16]
        url = "https://api.nasa.gov/EPIC/archive/natural/{}/{}/{}/png/{}.png?api_key={}".format(year, month, day, epic_id, token_epic)
        file_name = download_image(url, 'epic/epic_{}'.format(i))
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
    token_apod = os.getenv('API_EVERYDAY')
    token_epic = os.getenv("API_EPIC")
    lauch_id = os.getenv("LAUNCH_ID")
    fetch_nasa_day_pictures(args.day_pic, token_apod)
    fetch_nasa_epic_pictures(args.epic_pic, token_epic)
    fetch_spacex_last_launch(lauch_id)
