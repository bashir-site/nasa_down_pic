import requests
import os
from dotenv import load_dotenv
import argparse
from comon_code import download_image
from datetime import datetime


def fetch_nasa_epic_pictures(epic_token, count=5):
    response = requests.get('https://epic.gsfc.nasa.gov/api/natural')
    response.raise_for_status()

    pictures = []
    for image_number, image in enumerate(response.json()):
        if image_number == count:
            break
        image = image['image']
        date_str = image.replace("epic_1b_", "")[0:8]
        date_obj = datetime.strptime(date_str, '%Y%m%d')
        year, month, day = date_obj.year, date_obj.strftime('%m'), date_obj.day
        params = {
            "api_key": epic_token
        }
        url = "https://api.nasa.gov/EPIC/archive/natural/{}/{}/{}/png/{}.png".format(year, month, day, image)
        file_name = download_image(url, 'epic/epic_{}'.format(image_number), params)
        pictures.append(file_name)
    return pictures


if __name__ == "__main__":
    if not os.path.exists('epic'):
        os.makedirs('epic')

    parser = argparse.ArgumentParser(description='Программа загрузит EPIC фото в указаном количестве.')
    parser.add_argument('-count', metavar='count', type=int, default=5, help='Количество загружаемых фото')
    args = parser.parse_args()

    load_dotenv()
    epic_token = os.getenv("EPIC_TOKEN")

    fetch_nasa_epic_pictures(epic_token, args.count)
