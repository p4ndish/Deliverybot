from datetime import datetime
import os
from aiogram.filters import Command
from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, ReplyKeyboardRemove
import requests
from bot.database.functions import get_profile
from bot.keyboards import inline_keyboards, reply_keyboards
from bot.utils.backend_request import *
from bot.utils.shared_functions import refresh_login_callback, save_user_image, send_inline_providers
from bot.utils.states import RegisterDelivery, Shop
from bot.bot_instance import bot
from aiogram.types import MenuButtonWebApp, MenuButtonCommands, MenuButtonCommands, BotCommand
from aiogram.types.web_app_info import WebAppInfo


delivery_router = Router()


@delivery_router.callback_query(lambda c: c.data.startswith("iamdelivery_guy"))
async def start_registration(
    call: types.CallbackQuery,
    state: FSMContext,
):
    print("in delivery person registration...")
    _, userId = call.data.split("|")
    username = call.message.from_user.username
    await state.update_data(is_d_working=False)
    user_data = await state.get_data()

    print("saved user data:", user_data, user_data["userId"])
    # todo: check userid exists in delivery database if so just return weather the guy is free or not
    await call.message.answer(f"Welcome, {username}👋, to our delivery service. register to delivery products to users ")
    # userId = int(userId)
    # username = call.message.from_user.username
    # firstName = call.message.from_user.first_name
    # lastName = call.message.from_user.last_name
    # userImg = await bot.get_user_profile_photos(userId, offset=0, limit=1)
    # userImg = userImg.file_id
    # userImg = userImg.photos[0][-1] if userImg.photos else "https://gravatar.com/avatar/e4658044633caecd0563298a1be6d499?s=400&d=robohash&r=x"
    await state.set_state(RegisterDelivery.phoneNumber)

    # await state.update_data(userId=userId, userName=username, userImg=userImg, firstName=firstName, lastName=lastName, photoImg=userImg)
    await call.message.answer(
        "Please enter your phone number or press `Get My Number` ",
        parse_mode="MarkdownV2",
        reply_markup=inline_keyboards.register_phone_refrence_keyboard,
    )


@delivery_router.callback_query(
    lambda c: c.data == "get_my_number_inline", RegisterDelivery.phoneNumber
)
async def handle_register_phone_inline_callback(call: CallbackQuery, state: FSMContext):
    # if call.data == 'get_my_number_inline':
    print("in delivery register_phone_inline clicked")
    await state.set_state(RegisterDelivery.phoneNumber)
    await call.message.delete()
    await call.message.answer(
        "Please provide Your Phone Number", reply_markup=reply_keyboards.register_phone
    )


@delivery_router.callback_query(lambda c: c.data == "get_my_location_inline")
async def handle_register_phone_inline_callback(call: CallbackQuery, state: FSMContext):
    # if location is triggered
    # elif call.data == 'get_my_location_inline':
    await state.set_state(RegisterDelivery.location)
    await call.message.delete()
    await call.message.answer(
        "Please provide your location as it help us deliver our products",
        reply_markup=reply_keyboards.register_location,
    )


@delivery_router.message(F.contact, RegisterDelivery.phoneNumber)
async def get_phone_number(message: types.Message, state: FSMContext):
    ReplyKeyboardRemove()
    print("Now in delivery phone state")
    user_phoneNumber = message.contact.phone_number

    if user_phoneNumber == None:
        await state.set_state(RegisterDelivery.phoneNumber)
        await message.answer(
            "Please Provide a valid phone number",
            reply_markup=reply_keyboards.register_phone,
        )
    else:
        await state.set_state(RegisterDelivery.location)
        await state.update_data(phoneNumber=user_phoneNumber)
        msg = "Please provide your location as it help us deliver our products \n if you want to share your location later on press **Skip For Now** \n ⚠️use your phone ".replace(
            "*", "\*"
        )
        ReplyKeyboardRemove()
        await message.answer(
            msg,
            parse_mode="MarkdownV2",
            reply_markup=inline_keyboards.register_location_refrence_keyboard,
        )


@delivery_router.message(
    F.content_type.in_({"location", "LOCATION"}), RegisterDelivery.location
)
async def get_location_handler(message: types.Message, state: FSMContext):
    print("now on delivery location")
    user_location = message.location

    if not user_location:
        await message.answer(
            "please use your phone inorder for us to get your location, after that click on the below button",
            reply_markup=inline_keyboards.register_location_refrence_keyboard,
        )
        return

    await state.update_data(
        longtiude=user_location.longitude, latitude=user_location.latitude
    )
    date = datetime.now().isoformat()
    await state.update_data(created_at=date)
    await state.update_data(created_at=date)
    user_data = await state.get_data()
    # register user to db
    is_registered = await delivery_exists(message.from_user.id)
    if not is_registered:
    
        success = await register_delivery_profile(user_data)
        print(success == 201)
        print(dir(success))
        if success.status_code == 201:
            await save_user_image(message.from_user.id)
            await message.delete()
            await state.clear()
            await bot.set_my_commands( commands=[BotCommand(command='start', description='start delivery user'), BotCommand(command='menu', description='display menu'), BotCommand(command='profile', description='show profile page')])
            await bot.set_chat_menu_button(chat_id=message.from_user.id,
                    menu_button=MenuButtonCommands()
                )

            inline_job_options = inline_keyboards.delivery_person_menu_keyboard(
                False, False
            )
            await message.answer(
                text="<blockquote> ✅Registration successful. </blockquote>\n"
                "<b>Here is what will happen: \n"
                "1. If you want to get call first of all \n\t\t "
                "- you should share your location\n\t\t"
                "-  Click on\t\t\t <blockquote><u>I am free</u> Button</blockquote>\n\t\t"
                "2. If you are delivering products to user, please Click on \t\t\t <blockquote><u>am Working</u> Button</blockquote>  </b>",
                parse_mode="HTML",
                reply_markup=inline_job_options,
            )
    else: 
        state_data = await state.get_data()
        userId = state_data["userId"]
        isWorking = await is_user_working(userId)
        isWorking = isWorking[0]
        print("printing result from my status: ", isWorking)
        is_offline = await is_user_offline(userId)
        is_offline = is_offline[0]
        result = await get_delivery_user_status(userId)
        keyboard = inline_keyboards.delivery_person_menu_keyboard(
            isWorking["working"], is_offline["is_offline"]
        )
        await message.answer(
            text="<blockquote> Welcome Back. </blockquote>\n"
            "<b>Reminder on your what you will do here: \n"
            "1. If you want to get call first of all \n\t\t "
            "- you should share your location\n\t\t"
            "-  Click on\t\t\t <blockquote><u>I am free</u> Button</blockquote>\n\t\t"
            "2. If you are delivering products to user, please Click on \t\t\t <blockquote><u>am Working</u> Button</blockquote>  </b>",
            parse_mode="HTML",
            reply_markup=keyboard,
        )

        # await state.set_state(.shopping)
    # await message.answer('test remove', reply_markup=ReplyKeyboardRemove(remove_keyboard=True))

    await state.update_data(userId=message.from_user.id, role='deliveryGuy')


@delivery_router.callback_query(lambda c: c.data == "freeGuy")
async def handle_freeguy(call: CallbackQuery, state: FSMContext):
    await bot.set_my_commands( commands=[BotCommand(command='start', description='start over'), BotCommand(command='menu', description='display menu'), BotCommand(command='profile', description='show profile page')])
    await bot.set_chat_menu_button(chat_id=call.message.from_user.id,menu_button=MenuButtonCommands())
    # state_data = await state.get_data()
    # print("state_data: ", state_data)
    # if not state_data:
    #     print("user state not found, refreshing to login")
    #     await refresh_login_callback(call, state)
    #     state_data = await state.get_data()
    #     print("state_data: ", state_data)
    # # if the user is not working make it available for work
    # print("aren't they the same", call.message.from_user.id, call.id)

    state_data = await state.get_data()
    userId = state_data["userId"] if state_data else call.from_user.id
    result = await is_user_working(userId)
    is_offline = await is_user_offline(userId)
    result = result[0]
    is_offline = is_offline[0]
    if not result["working"] and is_offline["is_offline"]:
        """
        cases : he was offline
              :
        changes : update user to online status
        """
        data = {"user_id": userId, "to_": (not is_offline["is_offline"])}
        await update_user_onoff_status(userid=userId, data=data)
        await bot.answer_callback_query(
            callback_query_id=call.id,
            text="You will notified when their is a job",
            show_alert=True,
            cache_time=5,
        )
        inline_job_menu = inline_keyboards.delivery_person_menu_keyboard(
            False, (not is_offline["is_offline"])
        )
        await call.message.edit_reply_markup(
            text=call.message.text, reply_markup=inline_job_menu
        )
    # if not result['working']:
    #         await bot.answer_callback_query(text="You will notified when their is a job", show_alert=True, cache_time=5)
    else:
        await bot.answer_callback_query(
            callback_query_id=call.id,
            text="I said you will be notified, tf -_- ",
            show_alert=True,
            cache_time=5,
        )

    print(result)


@delivery_router.callback_query(lambda c: c.data == "stopWorking")
async def handle_freeguy(call: CallbackQuery, state: FSMContext):
    """
    if the user wantts to stop working
    - check if they are not working
      -> then update the is_offline to true

    """
    state_data = await state.get_data()
    userId = state_data["userId"]
    result = await is_user_working(userId)
    result = result[0]
    print("printing result from go offline: ", result)
    is_offline = await is_user_offline(userId)
    is_offline = is_offline[0]
    print("is offline from go offline", is_offline)
    data = {"user_id": userId, "to_": (not is_offline["is_offline"])}
    if not result["working"] and not is_offline["is_offline"]:
        await update_user_onoff_status(userId, data)
        inline_job_options = inline_keyboards.delivery_person_menu_keyboard(
            result["working"], (not is_offline["is_offline"])
        )

        await call.message.edit_reply_markup(call.id, reply_markup=inline_job_options)

    else:
        await bot.answer_callback_query(
            text="You are already offline what do you want ha",
            callback_query_id=call.id,
            show_alert=True,
            cache_time=5,
        )


@delivery_router.callback_query(lambda c: c.data == "WorkingGuy")
async def update_user_status_to_working(call: CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    userId = state_data["userId"]
    data = [{"userId": userId, "is_working": state_data["is_d_working"]}]
    result = await update_user_working_status(userId)


@delivery_router.callback_query(lambda c: c.data == "searchJob")
async def handle_freeguy(call: CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(
        text="You will be notified, Soon", callback_query_id=call.id, cache_time=10
    )  # bot.answer("")


@delivery_router.callback_query(lambda c: c.data == "triggerRelyProfile")
async def handle_freeguy(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    userId = data["userId"]
    keyboard = reply_keyboards.delivery_profile_menu(call.from_user.id)

    await call.message.answer(text="Edit Your Profile 👇", reply_markup=keyboard)


@delivery_router.callback_query(lambda c: c.data == "readMe")
async def handle_freeguy(call: CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    userId = state_data["userId"]
    result = await is_user_working(userId)
    result = result[0]
    print("printing result from go offline: ", result)
    is_offline = await is_user_offline(userId)
    is_offline = is_offline[0]
    print("is offline from readmMe", is_offline)
    data = {"user_id": userId, "to_": (not is_offline["is_offline"])}
    keyboard = inline_keyboards.delivery_person_menu_keyboard(
        result["working"], is_offline["is_offline"]
    )
    await call.message.edit_text(
        text="<b>Here is How It Works, \n"
        "1. If you want to get call first of all \n\t\t "
        "- you should share your location\n\t\t"
        "-  Click on\t\t\t <blockquote><u>I am free</u> Button</blockquote>\n\t\t"
        "2. If you are delivering products to user, please Click on \t\t\t <blockquote><u>am Working</u> Button</blockquote>  </b>",
        reply_markup=keyboard,
    )


@delivery_router.callback_query(lambda c: c.data == "myStatus")
async def handle_freeguy(call: CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    userId = state_data["userId"]
    isWorking = await is_user_working(userId)
    isWorking = isWorking[0]
    print("printing result from my status: ", isWorking)
    is_offline = await is_user_offline(userId)
    is_offline = is_offline[0]
    result = await get_delivery_user_status(userId)
    keyboard = inline_keyboards.delivery_person_menu_keyboard(
        isWorking["working"], is_offline["is_offline"]
    )
    msg = f"""<b>

    <u> User Status</u>
    Name: {result['firstName']}
    currently: <b>{"🟥 Offline" if result['is_offline'] else "🟩 Online"}</b>
    payed: {result['processed_amount']} Birr 
    pending payments: {result['pending_money']} Birr
    popularity: {result['ratings_sum']}

    </b>
    """
    await call.message.edit_text(text=msg, reply_markup=keyboard)


@delivery_router.callback_query(lambda c: c.data == "callDeliveryMenu")
async def handle_freeguy(call: CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    userId = state_data["userId"]

    result = await is_user_working(userId)
    result = result[0]
    print("printing result from callDelivery: ", result)
    is_offline = await is_user_offline(userId)
    is_offline = is_offline[0]
    keyboard = inline_keyboards.delivery_person_menu_keyboard(result, is_offline)
    await call.message.edit_text(
        text="<b>Here is How It Works, \n"
        "1. If you want to get call first of all \n\t\t "
        "- you should share your location\n\t\t"
        "-  Click on\t\t\t <blockquote><u>I am free</u> Button</blockquote>\n\t\t"
        "2. If you are delivering products to user, please Click on \t\t\t <blockquote><u>am Working</u> Button</blockquote>  </b>",
        reply_markup=keyboard,
    )
    await call.message.delete()


@delivery_router.message(F.text == "Delete Profile")
async def delete_profile_function(message: types.Message, state: FSMContext):
    await message.delete()
    s = await bot.get_chat(chat_id=message.from_user.id)
    print(s)
    state_data = await state.get_data()
    print("printing state ", state_data)
    userId = state_data["userId"]
    result = await delete_delivery_profile(userId)
    print(result)
    result = result[0]
    if result:
        await message.answer("profile deleted!")
        await state.clear()


@delivery_router.callback_query(lambda c: c.data.startswith("accept_order"))
async def accepted_order_function(call: CallbackQuery, state: FSMContext):
    _, order_id = call.data.split("|")
    print("in accepted order callback function", call.data)
    # accept order
    # fetch product details
    # fetch customer details and location

    await accept_order(call.from_user.id, order_id)
    products_detail = []
    products = await get_products_from_order_details(order_id)
    print("products to delivery: ", products)

    for product in products:
        s = await get_product(product["product_id"])
        products_detail.append(s)
    # print("products Detail: ", products_detail)
    customer_details = await get_customer_profile_details(order_id)
    # customer_details = customer_details[0]
    print("got customer details: ", customer_details)
    print("got product details: ", products_detail)
    print(products)

    msg = f"""
    Here are the order details 🔖 : \n\n
    """
    for idx, product in enumerate(products_detail):
        product = product[0]
        print("in loop:", idx, product)
        s = f"""<b>📌<u>Order #{idx}</u> \nproduct Name: {product['product_name']} \n\nproduct Description: {product['product_description']}\n\n\n\n 📍 Pick Item From: {product['product_service_provider']} </b>\n\n
        """
        msg += s 
    print('msg to send: ', msg)
    customer_image = customer_details['photoURL']
    longitude = customer_details['longtiude']
    latitude = customer_details['latitude']
    # customer_image = customer_details['latitude']
    profile_msg = f"""<b><u>👤User Deatil</u>\n
    FirstName: {customer_details['firstName']} \n 
    LastName: {customer_details['lastName'] if not customer_details['lastName'] == 'NULL' else '<del>None</del>' } \n
    Phone Number: <tg-spoiler>{customer_details['phoneNumber']} </tg-spoiler> \n

    Call Them : assure there address matches with the below 📍 location given </b>
    """
    await call.message.delete()
    await call.message.answer(text=msg, parse_mode="HTML")
    await call.message.answer_photo(photo=customer_image, caption=profile_msg)
    await call.message.answer_location(longitude=longitude, latitude=latitude)



@delivery_router.callback_query(lambda c: c.data.startswith("reject_order"))
async def reject_order(call: CallbackQuery, state: FSMContext):
    # remove the delivery guy id from the orders
    # await call.message.delete()
    bot.answer_callback_query(call.id, "Job skipped.")
        
    pass 
