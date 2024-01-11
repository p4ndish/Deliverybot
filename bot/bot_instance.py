import os
from aiogram import Bot, types
from dotenv import load_dotenv
load_dotenv()


bot = Bot(
    token=os.environ.get("BOT_TOKEN"),
    parse_mode='HTML'
)