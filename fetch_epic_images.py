import requests
import os
from dotenv import load_dotenv
from pathlib import Path
import argparse
from comon_code import download_image
from tele_bot import bot


if not os.path.exists('epic'):
    os.makedirs('epic')


def fetch_nasa_epic_pictures(count, token_epic):
    response = requests.get('https://epic.gsfc.nasa.gov/api/natural')
    response.raise_for_status()
    for i in range(count):
        epic_id = response.json()[i]['image']
        year, month, day = epic_id[8:12], epic_id[12:14], epic_id[14:16]
        params = {
            "api_key": token_epic
        }

        url = "https://api.nasa.gov/EPIC/archive/natural/{}/{}/{}/png/{}.png".format(year, month, day, epic_id)
        file_name = download_image(url, 'epic/epic_{}'.format(i), params)
        bot.send_document(chat_id=-997935206, document=open(file_name, 'rb'))


parser = argparse.ArgumentParser(description='Программа загрузит EPIC фото в указаном количестве.')
parser.add_argument('--count', metavar='count', type=int, help='Количество загружаемых фото')
args = parser.parse_args()

env_path = Path('.') / '.env'
load_dotenv()
token_epic = os.getenv("API_EPIC")

if args.count:
    fetch_nasa_epic_pictures(args.count, token_epic)
else:
    fetch_nasa_epic_pictures(5, token_epic)
