import os
from dotenv import load_dotenv
import argparse
from comon_code import send_telegram
from fetch_spacex_images import fetch_spacex_last_launch
from fetch_nasa_images import fetch_nasa_day_pictures
from fetch_epic_images import fetch_nasa_epic_pictures


if __name__ == "__main__":
    load_dotenv()
    telebot_token = os.getenv("TELEBOT_TOKEN")
    tg_chat_id = os.getenv('TG_CHAT_ID')
    apod_token = os.getenv('APOD_TOKEN')
    epic_token = os.getenv("EPIC_TOKEN")
    spacex_lauch_id = os.getenv("SPACEX_LAUNCH_ID")
    
    if not os.path.exists('images'):
        os.makedirs('images')

    if not os.path.exists('nasa'):
        os.makedirs('nasa')

    if not os.path.exists('epic'):
        os.makedirs('epic')

    parser = argparse.ArgumentParser(description='Программа скачивает NASA фотографии')
    parser.add_argument('-counta', metavar='amountD',  type=int, default=5, help='amount of everyday pictures that needs to download in directory nasa')
    parser.add_argument('-counte', metavar='amountE',  type=int, default=5, help='amount of epic pictures that needs to download in directory epic')
    parser.add_argument('-id', metavar='spacex_lauch_id', type=str, default=spacex_lauch_id, help='ID запуска')
    args = parser.parse_args()

    pictures_spacex = fetch_spacex_last_launch(spacex_lauch_id)
    pictures_day = fetch_nasa_day_pictures(apod_token, args.counta)
    pictures_epic = fetch_nasa_epic_pictures(epic_token, args.counte)
    for pictures in pictures_day, pictures_epic, pictures_spacex:
        send_photo_tg_bot(telebot_token, tg_chat_id, pictures)
