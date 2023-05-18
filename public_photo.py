import schedule
import os
import random
import telegram
from dotenv import load_dotenv


def send_photo(folder, shuffle):
    pictures_dir = os.listdir('{}/'.format(folder))
    if shuffle:
        file = random.shuffle(pictures_dir)
    for picture_number, picture in enumerate(pictures_dir):
        file = pictures_dir.pop(picture_number)
        print(file)
        with open('{}/{}'.format(folder, file), 'rb') as photo:
            bot.send_document(chat_id=tg_chat_id, document=photo)


if __name__ == "__main__":
    load_dotenv()
    telebot_token = os.getenv("TELEBOT_TOKEN")
    bot = telegram.Bot(token=telebot_token)
    tg_chat_id = os.getenv('TG_CHAT_ID')

    epic_folder, nasa_folder, images_folder = 'epic', 'nasa', 'images'

    try:
        schedule.every(2).seconds.do(send_photo, folder=epic_folder, shuffle=False)
    except IndexError:
        schedule.every(14400).seconds.do(send_photo, folder=epic_folder, shuffle=True)

    while True:
        schedule.run_pending()
