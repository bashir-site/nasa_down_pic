import requests
import os
import os.path
from urllib.parse import urlparse, urlencode
from dotenv import load_dotenv
import argparse
from datetime import datetime
from comon_code import download_image,send_telegram
from fetch_spacex_images import fetch_spacex_last_launch
from fetch_nasa_images import fetch_nasa_day_pictures
from fetch_epic_images import fetch_nasa_epic_pictures


if __name__ == "__main__":
    if not os.path.exists('images'):
        os.makedirs('images')

    if not os.path.exists('nasa'):
        os.makedirs('nasa')

    if not os.path.exists('epic'):
        os.makedirs('epic')

    parser = argparse.ArgumentParser(description='Программа скачивает NASA фотографии')
    parser.add_argument('--apod_count', metavar='amountD',  type=int, help='amount of everyday pictures that needs to download in directory nasa')
    parser.add_argument('--epic_count', metavar='amountE',  type=int, help='amount of epic pictures that needs to download in directory epic')
    args = parser.parse_args()

    load_dotenv()
    telebot_token = os.getenv("TELEBOT_TOKEN")
    apod_token = os.getenv('APOD_TOKEN')
    epic_token = os.getenv("EPIC_TOKEN")
    spacex_lauch_id = os.getenv("SPACEX_LAUNCH_ID")

    list_pictures_spacex = fetch_spacex_last_launch(spacex_lauch_id)
    list_pictures_day = fetch_nasa_day_pictures(apod_token, int(args.apod_count or 5))
    list_pictures_epic = fetch_nasa_epic_pictures(epic_token, int(args.epic_count or 5))
    for pictures in list_pictures_day, list_pictures_epic, list_pictures_spacex:
        send_telegram(telebot_token, pictures)

