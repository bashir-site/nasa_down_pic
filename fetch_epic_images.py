import requests
import os
from dotenv import load_dotenv
from urllib.parse import urlparse
from pathlib import Path
import argparse


if not os.path.exists('epic'):
	os.makedirs('epic')


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


def fetch_nasa_epic_pictures(count, api_epic):
	response = requests.get('https://epic.gsfc.nasa.gov/api/natural')
	response.raise_for_status()
	for i in range(count):
		epic_id = response.json()[i]['image']
		year = epic_id[8:12]
		month = epic_id[12:14]
		day = epic_id[14:16]
		url = "https://api.nasa.gov/EPIC/archive/natural/{}/{}/{}/png/{}.png?api_key={}".format(year, month, day,epic_id, api_epic)
		download_image(url, 'epic/epic_{}'.format(i))


parser = argparse.ArgumentParser(description='Программа загрузит EPIC фото в указаном количестве.')
parser.add_argument('--count', metavar='count', type=int, help='Количество загружаемых фото')
args = parser.parse_args()

env_path = Path('.') / '.env'
load_dotenv()
api_epic = os.getenv("API_EPIC")

if args.count:
	fetch_nasa_epic_pictures(args.count, api_epic)
else:
	fetch_nasa_epic_pictures(5, api_epic)

