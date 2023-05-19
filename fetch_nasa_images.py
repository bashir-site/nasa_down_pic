import requests
import os
from dotenv import load_dotenv
import argparse
from comon_code import download_image


def fetch_nasa_day_pictures(apod_token, count):
    params = {
        "api_key": apod_token,
        "count": count
    }
    url = "https://api.nasa.gov/planetary/apod"
    response = requests.get(url, params)
    response.raise_for_status()
    pictures = []
    for picture_number, picture in enumerate(response.json()):
        file_name = download_image(picture['url'], 'nasa/nasa_apod_{}'.format(picture_number), params)
        pictures.append(file_name)
    return pictures


if __name__ == "__main__":
    if not os.path.exists('nasa'):
        os.makedirs('nasa')
    
    parser = argparse.ArgumentParser(description='Программа загрузит фото от Nasa в указаном количестве.')
    parser.add_argument('-count', metavar='count', type=int, default=5, help='Количество загружаемых фото')
    args = parser.parse_args()

    load_dotenv()
    apod_token = os.getenv('APOD_TOKEN')
    fetch_nasa_day_pictures(apod_token, args.count)
