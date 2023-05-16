import requests
import os
from dotenv import load_dotenv
from pathlib import Path
import argparse
from main import download_image


if not os.path.exists('nasa'):
    os.makedirs('nasa')


def fetch_nasa_day_pictures(count, token_apod):
    params = {
        "api_key": token_apod,
        "count": count
    }
    url = "https://api.nasa.gov/planetary/apod"
    response = requests.get(url, params)
    response.raise_for_status()
    for i in range(count):
        file_name = download_image(response.json()[i]['url'], 'nasa/nasa_apod_{}'.format(i), params)
        bot.send_document(chat_id=-997935206, document=open(file_name, 'rb'))


parser = argparse.ArgumentParser(description='Программа загрузит фото от Nasa в указаном количестве.')
parser.add_argument('--count', metavar='count', type=int, help='Количество загружаемых фото')
args = parser.parse_args()

env_path = Path('.') / '.env'
load_dotenv()
token_apod = os.getenv('TOKEN_APOD')
if args.count:
    fetch_nasa_day_pictures(args.count, token_apod)
else:
    fetch_nasa_day_pictures(5, token_apod)
