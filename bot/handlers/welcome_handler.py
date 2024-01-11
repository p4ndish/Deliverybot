import os
from aiogram.filters import Command
from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
import requests
from bot.keyboards import inline_keyboards
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from bot.utils.shared_functions import prepare_image_url, register_user_data_in_state, send_inline_providers_command
from bot.bot_instance import bot
from bot.utils.states import Refresh, Register
import bot.handlers.welcome_handler
from aiogram.methods.delete_my_commands import DeleteMyCommands
welcome_router = Router()

@welcome_router.message(Command('start'))
async def handle_register(message : types.Message, state: FSMContext):
    print("am i in?")
    
    await register_user_data_in_state(message, state)
    # CHOOSE regular user or delivery guy 
    regular_user = InlineKeyboardButton(text="Regular User", callback_data=f"iamregular_user|{message.from_user.id}")
    delivery_user = InlineKeyboardButton(text="Delivery Guy", callback_data=f"iamdelivery_guy|{message.from_user.id}")

    # make them choose 
    choose_role_inline = InlineKeyboardMarkup(inline_keyboard=[
        [regular_user],
        [delivery_user],
        ], 
        resize_keyboard=True, one_time_keyboard=True
    )
    # todo : add some welcome photo 
    username = message.from_user.username
    await message.answer(f"Welcome, {username}👋, to our delivery service. we are delieghted to server you. Please Register to get start using our service")
    await message.answer(f"Choose Your Role, Are You...", reply_markup=choose_role_inline)

# @welcome_router.message(Command('start'))
# async def handle_start(message: types.Message, state: FSMContext):
#     # todo : add some welcome photo 
#     username = message.from_user.username
#     await message.answer(f"Welcome, {username}👋, to our delivery service. we are delieghted to server you. Please Register to get start using our service")
#     await state.set_state(Register.phoneNumber)



# @welcome_router.message(Command('another_thing'))
# async def handle_start(message: types.Message, state: FSMContext):
#     user_id = message.from_user.id
#     photos = await bot.get_user_profile_photos(user_id=user_id, offset=0, limit=1)
#     print(photos)
#     if photos.photos:
#         photo = photos.photos[0][-1]  # Get the last photo from the most recent profile photos
#         photo_file_id = photo.file_id
#         await message.reply_photo(photo=photo_file_id, caption="Here's your profile picture!", reply_markup=inline_keyboards.getting_started_keyboard)
#     else:
#         await message.reply_text("You don't have a profile picture.")


# @welcome_router.callback_query()
# async def handle_start(call: CallbackQuery, state: FSMContext):
#     if call.data == 'start_registering': 
#         url = "https://programmerhumor.io/wp-content/uploads/2021/06/programmerhumor-io-backend-memes-python-memes-2ce053f34837b43.png"
#         media = types.InputMediaPhoto(media=url, caption=call.message.caption)

#         # Make sure to complete the edit_media line
#         await call.message.edit_media(
#             inline_message_id=call.inline_message_id,
#             media=media, 
#             reply_markup=call.message.reply_markup
            
#         )
        

# @welcome_router.message(F.location)
# async def edit_live_location(message: types.Message):
#     # await bot.send
#     print("Edit live location: " )
#     pass

@welcome_router.message(Command('menu'))
async def menuu(message: types.Message, state: FSMContext):
    url = os.environ.get("APP_URL") + '/images/logo/zergawLogo.jpg'
    print("url for delivery", url)
    image = prepare_image_url(url)
    mainMenu = inline_keyboards.mainMenu(message.from_user.id)
    await message.answer_photo(photo=image, reply_markup=mainMenu)


@welcome_router.message(Refresh.get)
async def refresh_login(message: types.Message, state: FSMContext):
    await state.clear()
    await register_user_data_in_state(message, state)
    await message.answer("You are verified, continue with our service.")
    # TODO: check the role and send them their respective menu page 
    pass
