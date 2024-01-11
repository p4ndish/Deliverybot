from datetime import datetime
import os
from aiogram.filters import Command
from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
import requests
from bot.keyboards import inline_keyboards, reply_keyboards
from bot.bot_instance import bot 
from aiogram.types import CallbackQuery, InlineKeyboardButton, Message, MenuButtonCommands, BotCommand
from bot.database.functions import create_profile
from bot.utils.backend_request import user_exists
# from bot.middlewares.menu_builder_middleware import MenuMiddleware
from bot.utils.shared_functions import add_to_state_call, prepare_image_url, save_user_image, send_inline_providers
from bot.utils.states import Register, Shop
auth_router = Router(name='auth_router')

# auth_router.message.middleware(MenuMiddleware())
    
# @auth_router.callback_query()
# async def paginate(call: CallbackQuery, state: FSMContext):
#     print("callback found from: " + call.data)
#     print(dir(call))
    # id=await state.get_data()
    # print(id['id'])
    # if call.data == id['id']:
    #     print('found the paginator')



@auth_router.callback_query(lambda c: c.data.startswith("iamregular_user"))
async def get_start_with_normal_user(call : types.CallbackQuery, state: FSMContext, ):
    
    
    # await bot.answer_callback_query(text="Hoday ma friend", callback_query_id=call.id, cache_time=10)
    await bot.set_my_commands( commands=[])
    await bot.set_chat_menu_button(chat_id=call.message.from_user.id,
            menu_button=MenuButtonCommands()
        )
    _ , userId = call.data.split("|") 
    # userId = userId = int(userId)
    # username = call.message.from_user.username
    # firstName = call.message.from_user.first_name
    # lastName = call.message.from_user.last_name
    # userImg = await bot.get_user_profile_photos(userId, offset=0, limit=1) 
    # userImg = userImg.photos[0][-1] if userImg.photos else "https://gravatar.com/avatar/e4658044633caecd0563298a1be6d499?s=400&d=robohash&r=x"

    # print("user id ->>>> ",userId, firstName)
    # print("user image ->>>> ",userImg)
    await state.set_state(Register.phoneNumber)

    
    # await state.update_data(userId=userId, userName=username, userImg=userImg, firstName=firstName, lastName=lastName, photoImg=userImg) 
    await call.message.answer("Please enter your phone number or press `Get My Number` ", reply_markup=inline_keyboards.register_phone_refrence_keyboard)
    # await message.answer("", reply_markup=reply_keyboards.register_phone)











@auth_router.callback_query(lambda c: c.data == "get_my_number_inline", Register.phoneNumber)
async def handle_register_phone_inline_callback(call: CallbackQuery, state: FSMContext):
    # if call.data == 'get_my_number_inline':
    print("register_phone_inline clicked on regular user")
    await state.set_state(Register.phoneNumber)
    await call.message.delete()
    await call.message.answer("Please provide your number as it help us deliver our products", reply_markup=reply_keyboards.register_phone)

@auth_router.callback_query(lambda c: c.data == "get_my_location_inline", Register.location)
async def handle_register_phone_inline_callback(call: CallbackQuery, state: FSMContext):
    # if location is triggered 
    # elif call.data == 'get_my_location_inline':
    await state.set_state(Register.location)
    await call.message.delete()
    await call.message.answer("Please provide your location as it help us deliver our products", reply_markup=reply_keyboards.register_location)

        
@auth_router.callback_query(lambda c: c.data == "skip_location_inline", Register.location)
async def handle_register_phone_inline_callback(call: CallbackQuery, state: FSMContext):        
    # elif call.data == 'skip_location_inline':
    print("Skip location clicked on regular user")
    await call.message.answer("Alright we will do this later, keep in mind that it's necessary to provide your location")
    await state.update_data(longtiude="", latitude="")
    
    user_data = await state.get_data()
    if not user_data:
        await add_to_state_call(call, state)
    check_user = await user_exists(call.from_user.id)
    if check_user:
        await call.message.answer(text="user already exists! Continue with our service")
    else:
        success = await register_user(user_data,  call.message.from_user.first_name, call.message.from_user.last_name)
        if not success :
            await call.message.answer("<b>Sorry something went wrong, Try to provide your location or phone number.</b> \n <b>If the error persists</b> /start <b>over</b>",)
            return
        await save_user_image(call.from_user.id)
        await call.message.answer("✅Registration successful. You can now Start Purchase goods")

    await state.clear()
    
    # await call.message.answer("Choose your products", reply_markup=)
    await state.set_state(Shop.shopping)
    await state.update_data(userId=call.message.from_user.id )
    # await send_inline_providers(call, FSMContext)
    # setting menu buttons for customers 
    await bot.set_my_commands( commands=[BotCommand(command='start', description='start over'), BotCommand(command='menu', description='display menu'), BotCommand(command='profile', description='show profile page')])
    await bot.set_chat_menu_button(chat_id=call.message.from_user.id,
            menu_button=MenuButtonCommands()
        )
    # for later make the 
    url = os.environ.get("APP_URL") + '/images/logo/zergawLogo.jpg'
    print("url for delivery", url)
    image = prepare_image_url(url)
    mainMenu = inline_keyboards.mainMenu(call.message.from_user.id)
    await call.message.answer_photo(photo=image, reply_markup=mainMenu)


@auth_router.message(F.content_type.in_({'contact', 'CONTACT'}), Register.phoneNumber)
async def get_phone_number(message: types.Message, state: FSMContext):
    user_phoneNumber = message.contact.phone_number
    if user_phoneNumber == None:
        await state.set_state(Register.phoneNumber)
        await message.answer("Please Provide a valid phone number", reply_markup=reply_keyboards.register_phone)
    else:
        await state.set_state(Register.location)
        await state.update_data(phoneNumber=user_phoneNumber)
        msg = "Please provide your location as it help us deliver our products \n if you want to share your location later on press **Skip For Now** \n ⚠️use your phone ".replace('*', "\*")
        await message.answer(msg, parse_mode='MarkdownV2', reply_markup=inline_keyboards.register_or_skip_location_keyboard)



@auth_router.message(F.content_type.in_({'location', 'LOCATION'}), Register.location)
async def get_location_handler(message: types.Message, state: FSMContext):
    user_location = message.location

    if not user_location:
        await message.answer("please use your phone inorder for us to get your location, after that click on the below button", reply_markup=inline_keyboards.register_location_refrence_keyboard)
        return 
    
    await state.update_data(longtiude=user_location.longitude, latitude=user_location.latitude)
    user_data = await state.get_data()
    # register user to db
    check_user = await user_exists(message.from_user.id)
    if check_user:
        await message.answer(text="user already exists! Continue with our service")
    else:
        success = await register_user(user_data,  message.from_user.first_name, message.from_user.last_name)
        if not success :
            await message.answer("<b>Sorry something went wrong, Try to provide your location or phone number.</b> \n <b>If the error persists</b> /start <b>over</b>",)
            return
        await save_user_image(message.from_user.id)
        await message.answer("✅Registration successful. You can now Start Purchase goods")

    await state.clear()
    
    # await message.answer("Choose your products", reply_markup=)
    await state.set_state(Shop.shopping)
    await state.update_data(userId=message.from_user.id )
    # await send_inline_providers( FSMContext)
    # setting menu buttons for customers 
    await bot.set_my_commands( commands=[BotCommand(command='start', description='start over'), BotCommand(command='menu', description='display menu'), BotCommand(command='profile', description='show profile page')])
    await bot.set_chat_menu_button(chat_id=message.from_user.id,
            menu_button=MenuButtonCommands()
        )
    # for later make the 
    url = os.environ.get("APP_URL") + '/images/logo/zergawLogo.jpg'
    print("url for delivery", url)
    image = prepare_image_url(url)
    mainMenu = inline_keyboards.mainMenu(message.from_user.id)
    await message.answer_photo(photo=image, reply_markup=mainMenu)

    # if success:
         
    #     await state.clear()
    #     message.answer("✅Registration successful. You can now Start Purchase goods",)
    #     await state.set_state(Shop.shopping)
    #     await state.update_data(userId=message.from_user.id )
    #     await bot.set_my_commands( commands=[BotCommand(command='start', description='start over'), BotCommand(command='menu', description='display menu'), BotCommand(command='profile', description='show profile page')])
    #     await bot.set_chat_menu_button(chat_id=message.from_user.id,
    #             menu_button=MenuButtonCommands()
    #         )
    #     # for later make the 
    #     url = os.environ.get("APP_URL") + '/images/logo/zergawLogo.jpg'
    #     print("url for delivery", url)
    #     image = prepare_image_url(url)
    #     mainMenu = inline_keyboards.mainMenu(message.from_user.id)
    #     await message.answer_photo(photo=image, reply_markup=mainMenu)
        # providers_keyboard = await inline_keyboards.inline_providers()
        # photo_path = os.path.join("bot", "medias", "delivery_providers.jpg")
        # animation = open(photo_path, 'rb').read()
        # media = types.BufferedInputFile(animation, filename=photo_path)
        # await message.answer_photo(photo=media, reply_markup=providers_keyboard)
    print("user location: ", user_location)
    


    


    

async def register_user(user_data, firstName, lastName):
    print(user_data)
    date_now = datetime.now().isoformat()
    status = await create_profile(
        user_id=str(user_data['userId']),
        firstName= user_data['firstName'] if user_data['firstName'] else firstName,
        lastName=user_data['lastName'] if user_data['lastName'] else lastName,
        photoURL= user_data['photoImg'],
        phoneNumber=user_data['phoneNumber'],
        longtiude=user_data['longtiude'],
        latitude=user_data['latitude'],
        created_at=date_now,
        
        
    )
    return status
