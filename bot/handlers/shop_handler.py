from datetime import datetime
import os
from aiogram.filters import Command
from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
import requests
from bot.database.functions import get_profile
from bot.keyboards import inline_keyboards, reply_keyboards
from bot.utils.backend_request import *
from bot.utils.shared_functions import prepare_image_url, send_inline_providers
from bot.utils.states import Shop
from bot.bot_instance import bot
from aiogram.types import MenuButtonWebApp, MenuButtonCommands
from aiogram.types.web_app_info import WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder



shop_router = Router()

# @shop_router.callback_query(Shop.shopping)
# async def handle_thing(call: CallbackQuery, state: FSMContext):
#     print("Got something: " ,call.data)
# @shop_router.callback_query()
# async def handle_thing(call: CallbackQuery, state: FSMContext):
#     print("waiting for something from callback: " ,call.data)

# @shop_router.()
# async def handle_thing(nessage: types.Message, state: FSMContext):
#     print("waiting for something from message handler " )
    

@shop_router.callback_query(lambda c: c.data.startswith('service_providers'))
async def handle_show_providers(call: CallbackQuery, state: FSMContext):
    
    print("in the service provider callback: ", call.data)
    provider = call.data.split('|')[-1]
    #make a request to the backed
    products = await get_products_by_providers(provider, page=1, per_page=3)
    await send_products_page(call, products, current_page=1, prProvider=provider)




@shop_router.callback_query(lambda c: c.data.startswith('pagination'))
async def process_callback_pagination(callback_query: types.CallbackQuery):
    # Extract page number from callback data
    _, service_provider, current_page = callback_query.data.split('|')
    
    current_page = int(current_page)
    # Fetch paginated data for the requested page
    products = await get_products_by_providers(service_provider, page=current_page, per_page=3)

    # Send the requested page
    await send_products_page(callback_query, products, current_page, service_provider)





@shop_router.callback_query(lambda c: c.data.startswith('view_product'))
async def process_callback_pagination(callback_query: types.CallbackQuery):
    print("in the view_product callback_query:::::")
    _,  product_id, service_provider = callback_query.data.split('|')

    product_data = await get_product(product_id)
    product_data = product_data[0]
    print("printing product: " , product_data)
    

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🚚 Order Now ", callback_data=f"order_now|{product_id}")],
        [InlineKeyboardButton(text=f"Add Peice ➕", callback_data=f"increment|0|{product_id}|{service_provider}" ), ],
        [InlineKeyboardButton(text=" Add To Cart 🛒" , callback_data=f"add_to_cart|{product_id}|1")],
        [InlineKeyboardButton(text="🔙 Go Back", callback_data=f"service_providers|{service_provider}")]
    ])
    # special_characters = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
    # escape_table = str.maketrans({char: f'\\{char}' for char in special_characters})
    text = f"ㅤㅤㅤ <b>{str(product_data['product_name']).replace('-', ' ')}  \n \n🎯 Product Description: {product_data['product_description']} \n🎯 Price: {product_data['product_price']} Birr  \n🎯 Product Service Providers: <a href='http://google.com/'> {product_data['product_service_provider']} </a> </b> "
    print(os.environ.get("APP_URL"))
    url = os.environ.get("APP_URL") + '/images/' + product_data['product_image_url']
    media = types.InputMediaPhoto(media=url, caption=text, parse_mode='HTML')
    await callback_query.message.edit_media(media=media, reply_markup=keyboard)

@shop_router.inline_query()
async def handle_inline_query(query: types.InlineQuery):
    print(query.query)
    
    q = query.query if query.query else ""
    if  q:
        query_result = await query_product(q) 
        if query_result:
            print("this is what i query: ", query_result)
            print("and query result is: ", query_result[0]['product_name'])
            text = types.InputTextMessageContent(message_text=query_result[0]['product_name'])
        else:
            text = types.InputTextMessageContent(message_text="No results")
    else:

        text = types.InputTextMessageContent(message_text="No results")
        texta = types.InputTextMessageContent(message_text="No results")

        res = types.InlineQ(id='1', title=text,input_message_content=texta)
        await bot.answer_inline_query(inline_query_id=query.id, results=[res], cache_time=3) #.answer.inline_query(query.id, results=[res], cache_ )




@shop_router.callback_query(lambda c: c.data.startswith('increment'))
async def handle_increment_product(call: CallbackQuery, state: FSMContext):
    _, curr, product_id,srvProvider = call.data.split('|')
    current_piece = int(curr) + 1 
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🚚 Order Now ", callback_data=f"order_now|{product_id}|{current_piece}")],
        [InlineKeyboardButton(text=f"Add Piece ➕", callback_data=f"increment|{current_piece}|{product_id}|{srvProvider}" ), ],
        [InlineKeyboardButton(text=" 🛒 Add To Cart " , callback_data=f"add_to_cart|{product_id}|{current_piece}")],
        # [InlineKeyboardButton(text="🚚 Checkout ", callback_data=f"checkout_now|{product_id}|{current_piece}")],
        [InlineKeyboardButton(text="🔙 Go Back", callback_data=f"service_providers|{srvProvider}")]
        # [InlineKeyboardButton(text="Back To Menu", callback_data=f"show_menu")]
    ])
    product_data = await get_product(product_id)
    
    print("prining product data: ",  product_data)
    product_data = product_data[0]

    text = f"ㅤ<b>{str(product_data['product_name']).replace('-', ' ')}  \n \n🎯 Product Description: {product_data['product_description']} \n🎯 Price: {product_data['product_price']} Birr  \n🎯 Product Service Providers: <a href='http://google.com/'> {product_data['product_service_provider']} </a>  \nCurrent Peice on the cart:  {str(current_piece)} </b>"
    photoUrl = os.environ.get("APP_URL") + '/images/' + product_data['product_image_url']
    media = types.InputMediaPhoto(media=photoUrl, caption=text, parse_mode='HTML')
    await call.message.edit_media(media=media, reply_markup=keyboard)



@shop_router.callback_query(lambda c: c.data.startswith('order_now'))
async def process_order(call: CallbackQuery, state: FSMContext):
    # select item 
    if len(call.data.split('|')) != 3:
        await bot.answer_callback_query(callback_query_id=call.id, text="Please Add a Peice First")
        return
    _, product_id, current_piece = call.data.split('|')
    # current_piece = 1 
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        # [InlineKeyboardButton(text=f"Add Peice➕", callback_data=f"increment|{current_piece}|{product_id}" ), ],
        [InlineKeyboardButton(text=" Proceed To Checkout 💳 ", callback_data=f"checkout_now|{product_id}|{current_piece}")],
        [InlineKeyboardButton(text="Back To Menu", callback_data=f"show_menu")]
    ])
    product_data = await get_product(product_id)
    print("prining product data: ",  product_data)
    product_data = product_data[0]
    text = f"ㅤ<b>{str(product_data['product_name']).replace('-', ' ')}  \n \n🎯 Product Description: {product_data['product_description']} \n🎯 Price: {product_data['product_price']} Birr  \n🎯 Product Service Providers: <a href='http://google.com/'> {product_data['product_service_provider']} </a>  \nCurrent Peice on the cart:  {str(current_piece)} </b>"
    photoUrl = os.environ.get("APP_URL") + '/images/' + product_data['product_image_url']
    media = types.InputMediaPhoto(media=photoUrl, caption=text, parse_mode='HTML')
    await call.message.edit_media(media=media, reply_markup=keyboard)





@shop_router.message(Command("profile"), )
async def profile_command_handler(message: types.Message, state: FSMContext):
    user_state = await state.get_data() 
    print("user data: ", user_state)
    if user_state['role'] == 'customer':
        keyboard =  inline_keyboards.myProfileInlines(message.from_user.id)
        photoUrl = os.environ.get("APP_URL") + '/images/logo/zergawLogo.jpg'
        media = prepare_image_url(photoUrl)
        await message.answer_photo(photo=media, reply_markup=keyboard)
    else: 
        data = await state.get_data()
        userId = data["userId"]
        keyboard = reply_keyboards.delivery_profile_menu(message.from_user.id)

        await message.answer(text="Edit Your Profile 👇", reply_markup=keyboard)





@shop_router.message(Command('menu'))
async def menuu(message: types.Message, state: FSMContext):
    

    user_state = await state.get_data()
    if user_state['role'] == 'customer':
        url = os.environ.get("APP_URL") + '/images/logo/zergawLogo.jpg'
        print("url for delivery", url)
        image = prepare_image_url(url)
        mainMenu = inline_keyboards.mainMenu(message.from_user.id)
        await message.answer_photo(photo=image, reply_markup=mainMenu)
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
            text="<blockquote>Aloha, quick. </blockquote>\n"
            "<b>Reminder on your what you will do here: \n"
            "1. If you want to get call first of all \n\t\t "
            "- you should share your location\n\t\t"
            "-  Click on\t\t\t <blockquote><u>I am free</u> Button</blockquote>\n\t\t"
            "2. If you are delivering products to user, please Click on \t\t\t <blockquote><u>am Working</u> Button</blockquote>  </b>",
            parse_mode="HTML",
            reply_markup=keyboard,
        )

        
        


@shop_router.callback_query(lambda c: c.data.startswith('myProfileInline'))
async def handle_show_menu(call: CallbackQuery, state: FSMContext):
    # select item 
    _, userId = call.data.split('|')
    userId = userId if userId else call.from_user.id
    keyboard =  inline_keyboards.myProfileInlines(userId)
    photoUrl = os.environ.get("APP_URL") + '/images/logo/zergawLogo.jpg'
    media = types.InputMediaPhoto(media=photoUrl, caption=call.message.caption)
    await call.message.edit_media(media=media, reply_markup=keyboard)

@shop_router.callback_query(lambda c: c.data.startswith('show_Mainmenu'))
async def handle_show_menu(call: CallbackQuery, state: FSMContext):
    url = os.environ.get("APP_URL") + '/images/logo/zergawLogo.jpg'
    print("url for delivery", url)
    image = types.InputMediaPhoto(media=url)
    mainMenu = inline_keyboards.mainMenu(call.message.from_user.id)
    await call.message.edit_media(media=image, reply_markup=mainMenu)

@shop_router.callback_query(lambda c: c.data.startswith('show_menu'))
async def handle_show_menu(call: CallbackQuery, state: FSMContext):
    # select item 
    # _, product_id = call.data.split('|')
    keyboard = await inline_keyboards.inline_providers()
    photoUrl = os.environ.get("APP_URL") + '/images/logo/zergawLogo.jpg'
    msg = "** Let's start, Choose your Delivery Provider and get well served**"
    media = types.InputMediaPhoto(media=photoUrl, caption=msg, parse_mode="MarkdownV2")
    await call.message.edit_media(media=media, reply_markup=keyboard)

  
async def send_products_page(callback, products, current_page, prProvider):
    if not products:
        await callback.message.answer("No products available.")
        return
    
    print("products to send: ", products)


    pr_service_provider = prProvider 

    keyboard =  InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=f"{product['product_name']}", callback_data=f"view_product|{product['product_id']}|{prProvider}")] for product in products 
    ], row_width=3)
    
    product_image_url = ""
    if current_page > 1 and len(products) == 3:
        print("In the two buttons case ...")
        builder = InlineKeyboardBuilder()
        for product in products:
            product_image_url = product['product_service_provider_image']
            print("assigning product image :", product['product_service_provider_image'])
            builder.row(InlineKeyboardButton(text=f"{product['product_name']}", callback_data=f"view_product|{product['product_id']}|{prProvider}")) 

        builder.row(InlineKeyboardButton(text="⬅️ Previous", callback_data=f"pagination|{prProvider}|{current_page - 1}"))
        builder.add(InlineKeyboardButton(text="Next ➡️ ", callback_data=f"pagination|{prProvider}|{current_page + 1}"))
        builder.row(InlineKeyboardButton(text="↩️ Back To Menu", callback_data=f"show_menu"))
        url = os.environ.get("APP_URL") + '/'  + product_image_url
        print(url)
        input_media_photo = types.InputMediaPhoto(media=url)
        # media = types.BufferedInputFile(input_media_photo, filename=photo_path)

        await callback.message.edit_media( media=input_media_photo, inline_message_id=callback.inline_message_id, reply_markup=builder.as_markup())
        return
    elif current_page > 1:
        # include the previous button 
        # make the buttons 

        keyboard.inline_keyboard.append([InlineKeyboardButton(text="⬅️ Previous", callback_data=f"pagination|{prProvider}|{current_page - 1}")])

    elif len(products) == 3:  # Adjust this condition based on your actual pagination logic
        keyboard.inline_keyboard.append([InlineKeyboardButton(text="Next ➡️", callback_data=f"pagination|{prProvider}|{current_page + 1}")])
    keyboard.inline_keyboard.append([InlineKeyboardButton(text="↩️Back To Menu", callback_data=f"show_menu")])
    
    url = os.environ.get("APP_URL") + '/' +  f'images/logo/logo_{prProvider}.png' 
    print('url to send:', prProvider, url)
    input_media_photo = types.InputMediaPhoto(media=url)
    # photo_path = 'bot\\handlers\\delivery_providers.jpg'
    # photo = open(photo_path, 'rb').read()
    
    # media = types.BufferedInputFile(input_media_photo,filename=f"{prProvider}.png")

    await callback.message.edit_media( media=input_media_photo, inline_message_id=callback.inline_message_id, reply_markup=keyboard)
