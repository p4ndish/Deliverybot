import os
from aiogram.types import KeyboardButton,ReplyKeyboardMarkup, MenuButtonCommands,ReplyKeyboardRemove
from aiogram.utils.keyboard import ReplyKeyboardBuilder, ButtonType
from aiogram.types.web_app_info import WebAppInfo
from aiogram.types.web_app_data import WebAppData
from dotenv import load_dotenv
load_dotenv()
ReplyKeyboardRemove()
APP_URL = os.environ.get('APP_URL')
reg_phone = KeyboardButton(text="Get My Number", request_contact=True )
reg_location = KeyboardButton(text="Get My Location", request_location=True)

test = MenuButtonCommands()

#make the keyboard buttons
register_phone = ReplyKeyboardMarkup(keyboard=[ [reg_phone] ], resize_keyboard=True, one_time_keyboard=True)
register_location = ReplyKeyboardMarkup(keyboard=[ [reg_location] ], resize_keyboard=True, one_time_keyboard=True)


# delivery guy main reply buttons 
def delivery_profile_menu(userId):
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text="View Profile", resize_keyboard=True, one_time_keyboard=True, web_app=WebAppInfo(url=f"{APP_URL}/delivery/profile_view/{userId}")))
    builder.add(KeyboardButton(text="Edit Profile", resize_keyboard=True, one_time_keyboard=True, web_app=WebAppInfo(url=f"{APP_URL}/delivery/profile_edit/{userId}")))
    builder.row(KeyboardButton(text="Delete Profile", resize_keyboard=True, one_time_keyboard=True, ))
    delivery_profile_menu_keyboard = builder.as_markup()
    return delivery_profile_menu_keyboard
# builder.from_markup(delivery_menu_buttons)