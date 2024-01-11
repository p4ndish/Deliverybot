from datetime import datetime
import os
from aiogram.filters import Command
from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
import requests
from bot.keyboards import inline_keyboards, reply_keyboards
from bot.bot_instance import bot 
from aiogram.types import CallbackQuery, InlineKeyboardButton, Message, MenuButtonCommands, BotCommand

from bot.utils.backend_request import *
from bot.utils.shared_functions import prepare_image_url
from bot.utils.states import Checkout


cart_router = Router()



@cart_router.callback_query(lambda c: c.data.startswith('show_cart'))
async def show_cart_inline(call: CallbackQuery, state: FSMContext):
    await state.set_state(Checkout.from_cart)
    # img with inline buttons 
    state_data = await state.get_data()
    # userid = state_data['user_id']
    keyboard = await inline_keyboards.show_cart_inline(call.from_user.id, 0)
    # result = await get_cart_items(call.from_user.id)
    url = os.environ.get("APP_URL") + '/images/logo/zergawLogo.jpg'
    # print("url for delivery", url)
    media = types.InputMediaPhoto(media=url,)
    await call.message.edit_media(media=media, reply_markup=keyboard)
    
@cart_router.callback_query(lambda c: c.data.startswith('add_to_cart'))
async def add_cart_inline(call: CallbackQuery, state: FSMContext):
    # img with inline buttons 
    print("call data", call.data)
    _, product_id,quantity = call.data.split('|')
    res = await add_to_cart(call.from_user.id, product_id, quantity)
    if res:
        await bot.answer_callback_query(callback_query_id=call.id, text='👍 Successfully added to cart')
    else:
        await bot.answer_callback_query(callback_query_id=call.id, text='⛔️ Something went wrong, try again')

    print("print got data from: ",res)
    
    # state_data = await state.get_data()
    # userid = state_data['user_id']
    # keyboard = inline_keyboards.show_cart_inline(call.from_user.id)


@cart_router.callback_query(lambda c: c.data.startswith('view_cart_product'))
async def view_cart_product(call: CallbackQuery, state: FSMContext):
    _, product_id, quantity = call.data.split('|')
    print('printing products to view: ', call.data)
    product_data = await get_product(product_id)
    product_data = product_data[0]
    keyboard = await inline_keyboards.show_cart_inline(call.from_user.id, product_data['product_id'])

    text = f"ㅤㅤㅤ <b><u>{str(product_data['product_name']).replace('-', ' ')} </u> \n \n🎯 Product Description: {product_data['product_description']} \n🎯 Price: {product_data['product_price']} Birr  \n🎯 Product Service Providers: <a href='http://google.com/'> {product_data['product_service_provider']} </a> \n\n\n Added Piece: {str(quantity)}</b> "
    print(os.environ.get("APP_URL"))
    url = os.environ.get("APP_URL") + '/images/' + product_data['product_image_url']
    media = types.InputMediaPhoto(media=url, caption=text, parse_mode='HTML')
    await call.message.edit_media(media=media, reply_markup=keyboard)





@cart_router.callback_query(lambda c: c.data.startswith("empty_cart"))
async def empty_cart_route(call: CallbackQuery, state: FSMContext):
    _, user_id = call.data.split('|')
    stat = await delete_user_cart(user_id)
    if stat: 
        await bot.answer_callback_query(callback_query_id=call.id, text="✅ Cart Items deleted successfully")
    url = os.environ.get("APP_URL") + '/images/logo/zergawLogo.jpg'
    print("url for delivery", url)
    image = prepare_image_url(url)
    mainMenu = inline_keyboards.mainMenu(call.message.from_user.id)
    await call.message.delete()
    await call.message.edit_media(photo=image, reply_markup=mainMenu)
    