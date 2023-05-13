import os
from dotenv import load_dotenv
from pathlib import Path
import telegram

env_path = Path('.') / '.env'
load_dotenv()
telebot_token = os.getenv("TELEBOT_TOKEN")

bot = telegram.Bot(token=telebot_token)

# updates = bot.get_updates()

# bot.send_message(text='Hello!', chat_id=-997935206)