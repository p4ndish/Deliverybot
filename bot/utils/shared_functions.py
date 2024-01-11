# functions that are shared between routers 
from aiogram.types import KeyboardButton,ReplyKeyboardMarkup, MenuButtonCommands, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram import types
import requests
from bot.database.functions import get_profile
from bot.keyboards import inline_keyboards
import os 
from bot.bot_instance import bot
from bot.utils.states import Refresh, RegisterDelivery 
from aiogram.types import URLInputFile


async def send_inline_providers(call, state):
    photo_path = os.path.join("bot", "medias", "delivery_providers.jpg")
    animation = open(photo_path, 'rb').read()
    media = types.BufferedInputFile(animation, filename=photo_path)
    # url = os.environ.get("APP_URL") + "/img/" + 'delivery_providers.jpg'
    # media = types.InputMediaPhoto(url)
    providers_keyboard = await inline_keyboards.inline_providers()
    await call.message.answer_photo(photo=media, reply_markup=providers_keyboard)
async def send_inline_providers_command(call, state):
    photo_path = os.path.join("bot", "medias", "delivery_providers.jpg")
    animation = open(photo_path, 'rb').read()
    media = types.BufferedInputFile(animation, filename=photo_path)
    # url = os.environ.get("APP_URL") + "/img/" + 'delivery_providers.jpg'
    # media = types.InputMediaPhoto(url)
    providers_keyboard = await inline_keyboards.inline_providers()
    await call.answer_photo(photo=media, reply_markup=providers_keyboard)

async def add_to_state_message(message, state):
    await state.update_date(userId=message.from_user.id)
async def add_to_state_call(call, state):
    await state.update_date(userId=call.from_user.id)
def prepare_image_url(url):
    image = URLInputFile(
        url=url,
        filename="python-logo.png"
    )
    return image


async def register_user_data_in_state(message, state):
    userId = message.from_user.id
    username = message.from_user.username if message.from_user.username else 'NULL'
    firstName = message.from_user.first_name if message.from_user.first_name else 'NULL'
    lastName = message.from_user.last_name if message.from_user.last_name else 'NULL'
    userImg = await bot.get_user_profile_photos(userId, offset=0, limit=1)
    if userImg.photos:
        userImg = userImg.photos[0][-1].file_id
    else:
        userImg = "https://gravatar.com/avatar/e4658044633caecd0563298a1be6d499?s=400&d=robohash&r=x"
    # await state.set_state(RegisterDelivery.phoneNumber)
    await state.update_data(userId=userId, userName=username, userImg=userImg, firstName=firstName, lastName=lastName, photoImg=userImg) 


async def save_user_image(userId):
    userImg = await bot.get_user_profile_photos(userId, offset=0, limit=1)    
    print(userImg.photos)
    if userImg.photos:
        userImg = userImg.photos[0][-1] 
        s = await bot.get_file(userImg.file_id)
        await bot.download_file(s.file_path, destination=f"web_service/images/users_image/{userId}.jpg")
        print(userImg, dir(userImg))
    else:

        image_url = 'https://gravatar.com/avatar/e4658044633caecd0563298a1be6d499?s=400&d=robohash&r=x'
        response = requests.get(image_url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Replace 'local_image.jpg' with the desired local filename
            local_filename = f'web_service/images/users_image/{userId}.jpg'

            # Save the image content to a local file
            with open(local_filename, 'wb') as file:
                file.write(response.content)



async def refresh_login_callback(call, state):
    keyboard = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="Refresh Login",resize_keyboard=True, one_time_keyboard=True)]
    ])
    await state.set_state(Refresh.get)
    call.message.answer(text="Something went wrong please, refresh login", reply_keyboard_markup=keyboard)
    


async def refresh_login_message(message, state):
    # get the user id 
    userId = message.from_user.id 
    
    # verify user exists in db 
    user_result = await get_profile(userId)
    if not user_result:
        # send the user to choose role
        await state.clear() 
        await register_user_data_in_state(message, state)
        bot.send_message("Your Are Not Registered, Please Register")
        regular_user = InlineKeyboardButton(text="Regular User", callback_data=f"iamregular_user|{message.from_user.id}")
        delivery_user = InlineKeyboardButton(text="Delivery Guy", callback_data=f"iamdelivery_guy|{message.from_user.id}")

        # make them choose 
        choose_role_inline = InlineKeyboardMarkup(inline_keyboard=[
            [regular_user],
            [delivery_user],
            ], 
            resize_keyboard=True, one_time_keyboard=True
        )
        await message.answer(text="Your Are Not Registered,  Please Register", reply_keyboard_markup=choose_role_inline)
    else:
        #if user exists 
        # update the state with necessary information
        # recall state.get_data()
        await state.clear() 
        await register_user_data_in_state(message, state)
        
        