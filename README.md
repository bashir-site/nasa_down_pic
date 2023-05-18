# NASA photos downloader

NASA photos downloader is a Python script for dealing with NASA picturies. The program find everyday and epic photos from NASA api  and  saves them in directory `epic` ,  `nasa`  and  `images`.

## Installation

First of all you need to download all the files in this repo to your computer. Then you need to create and run a virtual environment with these commands:

On Mac OS and Linux:
```bash
# create environment with name venv
virtualenv venv -p python3
# runing venv enviroment
source venv/bin/activate
```

On Windows:
```bash
# create environment with name env
python -m venv env
# runing env enviroment
env\Scripts\activate
```

The next step is to install the necessary modules. This command will help:
```bash
pip install -r requirements.txt
```


## Usage

You can run 4 files:
1. `main.py` - main file that downloads photos from all APIs at once and fills the folders `epic`, `nasa`, `images`
2. `fetch_nasa_images.py` - file which downloads photos only from the api nasa and loads them into the folder `nasa`
3. `fetch_epic_images.py` - the file that downloads photos only from the api epic and loads them into the `epic` folder
4. `fetch_space_images.py` - file that downloads photos only from api spacex and uploads them to the `images` folder

Before you run the script, you must specify the environment variables: 
1. APOD_TOKEN is the token for daily nasa(apod) photos. This token can be obtained from the website - https://api.nasa.gov/#apod . This token is needed to run the script `fetch_nasa_images.py`
2. EPIC_TOKEN is a token for taking nasa(EPIC) earth photos. You can get this token at https://api.nasa.gov/#epic . This token is needed to run the script `fetch_epic_images.py`
3. SPACEX_LAUNCH_ID is the id of the best photo of the day. This token is needed to run the script `fetch_space_images.py`
4. TELEBOT_TOKEN is the token you get after registration with BotFather.
5. TG_CHAT_ID is the chat ID where bot will send messages.


To run the `main.py` file you need to write this command:

```bash
python main.py 6 6
```
this command download 6 pictures from apod api, 6 pictures from epic api and all pictures from spacex api.
After script complete, you've gonna see all picturies in directory `epic` ,  `nasa`  and  `images`.


To run the `fetch_nasa_images.py` file you need to write this command:

```bash
python fetch_nasa_images.py --count 4
```
this command download 4 pictures from apod api.
After script complete, you've gonna see all picturies in directory `nasa`


To run the `fetch_epic_images.py` file you need to write this command:

```bash
python fetch_epic_images.py --count 4
```
this command download 4 pictures from epic api.
After script complete, you've gonna see all picturies in directory `epic`


To run the `fetch_space_images.py` file you need to write this command:

with paramets --id:
```bash
python fetch_space_images.py --id {own_id}
```
Instead of {own_id} you have to put your id

or without:
```bash
python fetch_space_images.py 
```
then script just grab my own id

this command download 4 pictures from spacex api.
After script complete, you've gonna see all picturies in directory `images`

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## Project Goals
This code was written for educational purposes as part of an online course for web developers at dvmn.org.

## Contacts

You can find my on telegram: https://t.me/bashir_77