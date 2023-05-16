import requests
import os
import os.path
from urllib.parse import urlparse
from dotenv import load_dotenv
from pathlib import Path
import argparse


if not os.path.exists('images'):
	os.makedirs('images')

if not os.path.exists('nasa'):
	os.makedirs('nasa')

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
	

def fetch_spacex_last_launch(id):
	response = requests.get("https://api.spacexdata.com/v5/launches/{}".format(id))
	response.raise_for_status()
	pictures = response.json()['links']['flickr']['original']

	for i in range(0, len(pictures)):
		download_image(pictures[i], 'images/spacex_{}'.format(i))


def fetch_nasa_day_pictures(count, api_everyday):
	url = "https://api.nasa.gov/planetary/apod?count={}&api_key={}".format(count, api_everyday)
	response = requests.get(url)
	response.raise_for_status()
	for i in range(0, count):
		download_image(response.json()[i]['url'], 'nasa/nasa_apod_{}'.format(i))


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


if __name__ == "__main__":
		parser = argparse.ArgumentParser(description='Программа скачивает NASA фотографии')
		parser.add_argument('day_pic', metavar='amountD',  type=int, help='amount of everyday pictures that needs to download in directory nasa')
		parser.add_argument('epic_pic', metavar='amountE',  type=int, help='amount of epic pictures that needs to download in directory epic')
		args = parser.parse_args()

		env_path = Path('.') / '.env'
		load_dotenv()
		api_everyday = os.getenv('API_EVERYDAY')
		api_epic = os.getenv("API_EPIC")
		lauch_id = os.getenv("LAUNCH_ID")

		fetch_nasa_day_pictures(args.day_pic, api_everyday)
		fetch_nasa_epic_pictures(args.epic_pic, api_epic)
		fetch_spacex_last_launch(lauch_id)
		download_image("https://upload.wikimedia.org/wikipedia/commons/3/3f/HST-SM4.jpeg", 'images/space_ship')
	

  







