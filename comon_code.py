import requests
import os
from urllib.parse import urlparse
from tele_bot import bot


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
	bot.send_document(chat_id=-997935206, document=open(file_name, 'rb'))