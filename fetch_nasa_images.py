import requests
import os
from dotenv import load_dotenv
from urllib.parse import urlparse
from pathlib import Path
import argparse


if not os.path.exists('nasa'):
	os.makedirs('nasa')


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


def fetch_nasa_day_pictures(count, api_everyday):
	url = "https://api.nasa.gov/planetary/apod?count={}&api_key={}".format(count, api_everyday)
	response = requests.get(url)
	response.raise_for_status()
	for i in range(0, count):
		download_image(response.json()[i]['url'], 'nasa/nasa_apod_{}'.format(i))


parser = argparse.ArgumentParser(description='Программа загрузит фото от Nasa в указаном количестве.')
parser.add_argument('--count', metavar='count', type=int, help='Количество загружаемых фото')
args = parser.parse_args()

env_path = Path('.') / '.env'
load_dotenv()
api_everyday = os.getenv('API_EVERYDAY')
if args.count:
	fetch_nasa_day_pictures(args.count, api_everyday)
else:
	fetch_nasa_day_pictures(5, api_everyday)