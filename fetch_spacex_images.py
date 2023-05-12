import requests
import os
from dotenv import load_dotenv
from urllib.parse import urlparse
from pathlib import Path
import argparse


if not os.path.exists('images'):
	os.makedirs('images')


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


def fetch_spacex_last_launch(id):
	response = requests.get("https://api.spacexdata.com/v5/launches/{}".format(id))
	response.raise_for_status()
	pictures = response.json()['links']['flickr']['original']

	for i in range(0, len(pictures)):
		download_image(pictures[i], 'images/spacex_{}'.format(i))


parser = argparse.ArgumentParser(description='Программа загрузит фото от SpaceX по указанному ID запуска.')
parser.add_argument('--id', metavar='amountD', help='ID запуска')
args = parser.parse_args()

if args.id:
	fetch_spacex_last_launch(args.id)
else:
	env_path = Path('.') / '.env'
	load_dotenv()
	lauch_id = os.getenv("LAUNCH_ID")
	fetch_spacex_last_launch(lauch_id)
