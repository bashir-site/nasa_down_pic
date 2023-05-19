import schedule
import os
import random
import telegram
from dotenv import load_dotenv


class EmptyListError(Exception):
    def __init__(self, text):
        self.txt = text


def send_photo(folder, shuffle):
    pictures_dir = os.listdir('{}/'.format(folder))
    if shuffle:
        file = random.shuffle(pictures_dir)
    for picture_number, picture in enumerate(pictures_dir):
        if pictures_dir == []:
            raise EmptyListError("Список фотогафий пуст!")
        file = pictures_dir.pop(picture_number)
        with open('{}/{}'.format(folder, file), 'rb') as photo:
            bot.send_document(chat_id=tg_chat_id, document=photo)


if __name__ == "__main__":
    load_dotenv()
    telebot_token = os.getenv("TELEBOT_TOKEN")
    bot = telegram.Bot(token=telebot_token)
    tg_chat_id = os.getenv('TG_CHAT_ID')

    epic_folder, nasa_folder, images_folder = 'epic', 'nasa', 'images'

    try:
        schedule.every(14400).seconds.do(send_photo, folder=epic_folder, shuffle=False)
    except EmptyListError as elr:
        schedule.every(14400).seconds.do(send_photo, folder=epic_folder, shuffle=True)

    while True:
        schedule.run_pending()
