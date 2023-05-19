import os
from dotenv import load_dotenv
import argparse
import schedule
import time
import random
from comon_code import send_photo_tg_bot
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

    os.makedirs('images', exist_ok=True)
    os.makedirs('nasa', exist_ok=True)
    os.makedirs('epic', exist_ok=True)

    parser = argparse.ArgumentParser(description='Программа скачивает NASA фотографии')
    parser.add_argument('-counta', metavar='amountD',  type=int, default=5, help='amount of everyday pictures that needs to download in directory nasa')
    parser.add_argument('-counte', metavar='amountE',  type=int, default=5, help='amount of epic pictures that needs to download in directory epic')
    parser.add_argument('-id', metavar='spacex_lauch_id', type=str, default=spacex_lauch_id, help='ID запуска')
    args = parser.parse_args()

    pictures_spacex = fetch_spacex_last_launch(args.id)
    pictures_day = fetch_nasa_day_pictures(apod_token, args.counta)
    pictures_epic = fetch_nasa_epic_pictures(epic_token, args.counte)
    all_pictures = pictures_spacex + pictures_day + pictures_epic
    random.shuffle(all_pictures)
    
    for picture in all_pictures:
        schedule.every(4).hour.do(send_photo_tg_bot, telebot_token=telebot_token,tg_chat_id=tg_chat_id,file_name=picture)

    while True:
        schedule.run_pending()