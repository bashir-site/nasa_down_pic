import requests
import os
from dotenv import load_dotenv
from pathlib import Path
import argparse
from comon_code import download_image


if not os.path.exists('images'):
	os.makedirs('images')


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
