import requests
import os
from urllib.parse import urlparse, urlencode


def get_file_extension(link):
    file = urlparse(link)
    extension = os.path.splitext(file.path)
    return extension[1]


def download_image(link, name, payload={}):
    payload = urlencode(payload)
    response = requests.get(link, params=payload)
    response.raise_for_status()
    url = get_file_extension(link)
    file_name = '{}{}'.format(name, url)
    with open(file_name, 'wb') as file:
        file.write(response.content)

    return file_name
