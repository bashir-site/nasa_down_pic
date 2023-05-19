import schedule
import os
import random
import telegram
from dotenv import load_dotenv


class EmptyListError(Exception):
    def __init__(self, text):
        self.txt = text


def send_photos(all_pictures, shuffle):
    if shuffle:
        file = random.shuffle(all_pictures)
    for picture_number, picture in enumerate(all_pictures):
        if all_pictures == []:
            raise EmptyListError("Список фотогафий пуст!")
        file = all_pictures.pop(picture_number)
        with open(file, 'rb') as photo:
            bot.send_document(chat_id=tg_chat_id, document=photo)


if __name__ == "__main__":
    load_dotenv()
    telebot_token = os.getenv("TELEBOT_TOKEN")
    bot = telegram.Bot(token=telebot_token)
    tg_chat_id = os.getenv('TG_CHAT_ID')

    pictures_epic_dir = [os.path.join('epic', filename) for filename in os.listdir('epic')]
    pictures_nasa_dir = [os.path.join('nasa', filename) for filename in os.listdir('nasa')]
    pictures_images_dir = [os.path.join('images', filename) for filename in os.listdir('images')]
    all_pictures = pictures_epic_dir + pictures_nasa_dir + pictures_images_dir

    try:
        schedule.every(2).seconds.do(send_photos, all_pictures=all_pictures, shuffle=False)
    except EmptyListError:
        schedule.every(14400).seconds.do(send_photos, all_pictures=all_pictures, shuffle=True)

    while True:
        schedule.run_pending()
