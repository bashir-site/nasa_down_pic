import schedule
import requests
import os
from tele_bot import bot
import random


def send_photo():
    for i in range(1):
        file = epic.pop(i)
        bot.send_document(chat_id=-997935206, document=open('epic/'+file, 'rb'))


def shuffle_photo():
    for i in range(4):
        file = random.shuffle(epic)
        file  = file.pop(i)
        bot.send_document(chat_id=-997935206, document=open('epic/'+file, 'rb'))


def main():
    epic = os.listdir('epic/')
    nasa = os.listdir('nasa/')
    images = os.listdir('images/')

    try:
        schedule.every(14400).seconds.do(send_photo)
    except:
        schedule.every(14400).seconds.do(shuffle_photo)

    while True:
        schedule.run_pending()


main()