import os
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from aiogram.types.menu_button import MenuButton
from aiogram_widgets.pagination import KeyboardPaginator
from bot.database.functions import *
from aiogram.types.web_app_info import WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.utils.backend_request import get_cart_items, get_product

editProfile = os.environ.get("APP_URL") + '/u/profile/edit/'
showProfile = os.environ.get("APP_URL") + '/u/profile/show/'
BASE_URL = os.environ.get("APP_URL")
# t = MenuButton(text="Toggle", web_app=WebAppInfo(url="https://1051-196-190-62-170.ngrok-free.app/"))

test_webapp = KeyboardButton(text="Open Web", web_app=WebAppInfo(url=os.environ.get('APP_URL')))
inline_webapp = ReplyKeyboardMarkup(keyboard=[[test_webapp]], resize_keyboard=True, one_time_keyboard=True)
#inline welcome keyboards 
get_start_keyboard = InlineKeyboardButton(text="Register", callback_data="start_registering")
policy_show_keyboard = InlineKeyboardButton(text='read our policy', callback_data='read_policy')
reg_phone = InlineKeyboardButton(text="Get My Number", callback_data="get_my_number_inline")
reg_location = InlineKeyboardButton(text="Get My Location", callback_data="get_my_location_inline")
skip_location = InlineKeyboardButton(text="Skip Location", callback_data="skip_location_inline")
cancel_checkout = InlineKeyboardButton(text="Cancel", callback_data="cancel_checkout_inline")
order_completed = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Order Completed", callback_data="order_completed_inline")]])





# inline menu buttons
async def inline_providers():
    companies = await get_providers()
    print("snippet, ",companies[0])
    service_providers_inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=f"{company['product_service_provider']}", callback_data=f"service_providers|{company['product_service_provider']}")] for company in companies 
    ])
    return service_providers_inline_keyboard

# service_providers_inline_keyboard = await inline_providers()
previous_menu_btn = InlineKeyboardButton(text="<<Prev", callback_data="paginate|backward")

next_menu_btn = InlineKeyboardButton(text="Next >>", callback_data="paginate|forward")
# main menu 
def mainMenu(userId):
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="Shop Now 🛍", callback_data="show_menu"))
    builder.row(InlineKeyboardButton(text="👤 Profile", callback_data=f"myProfileInline|{userId}"))
    builder.add(InlineKeyboardButton(text="My Cart 🛒", callback_data=f"show_cart|{userId}"))
    builder.row(InlineKeyboardButton(text="Play and Earn 🎮", callback_data="show_play_earn"))
    builder.row(InlineKeyboardButton(text="About Us 🔖", web_app=WebAppInfo(url=BASE_URL + '/aboutus')))
    builder.add(InlineKeyboardButton(text="Privacy and Policy 🔐", web_app=WebAppInfo(url=BASE_URL + '/privacy')))

    mainMenu = builder.as_markup()
    return mainMenu

# user profile inlines
def myProfileInlines(userId):
    userId = str(userId)
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="Show Profile", web_app=WebAppInfo(url=showProfile + userId)))
    builder.add(InlineKeyboardButton(text="Edit Profile", web_app=WebAppInfo(url=editProfile + userId) ))
    builder.row(InlineKeyboardButton(text="Delete Profile", callback_data="user_delete_profile"))
    builder.row(InlineKeyboardButton(text="↩️ Back To Menu", callback_data=f"show_Mainmenu"))

    inline_my_profile_list = builder.as_markup()
    return inline_my_profile_list

# show_user_profile_inline_btn = 

# make the keyboard
getting_started_keyboard = InlineKeyboardMarkup(inline_keyboard=[[get_start_keyboard], [policy_show_keyboard]], resize_keyboard=True, one_time_keyboard=True)
register_phone_refrence_keyboard = InlineKeyboardMarkup(inline_keyboard=[[reg_phone]], resize_keyboard=True, one_time_keyboard=True)
register_location_refrence_keyboard = InlineKeyboardMarkup(inline_keyboard=[ [reg_location]], resize_keyboard=True, one_time_keyboard=True)
register_or_skip_location_keyboard = InlineKeyboardMarkup(inline_keyboard=[[reg_location], [skip_location]], resize_keyboard=True, one_time_keyboard=True)
inline_checkout_cancel_keyboard = InlineKeyboardMarkup(inline_keyboard=[[cancel_checkout]], resize_keyboard=True, one_time_keyboard=True, row_width=1)
# make user profile inlines 
# show_user_profile_inline = InlineKeyboardMarkup(inline_keyboard=[[show_user_profile_inline_btn]], resize_keyboard=True, one_time_keyboard=True)





# delivery person settings 

def delivery_person_menu_keyboard(isWorking, isOffline):
    builder = InlineKeyboardBuilder()
    if not isWorking and not isOffline:
        text1 = "🟢 Open For Work"
        text2 = "I Am Working (deliverying)"
        text3 = "Go Offline"
    elif isWorking and (not isOffline):
        text1 = "Open For Work"
        text2 = "🟢 I Am Working (deliverying)"
        text3 = "Go Offline"
        
    elif not isWorking and isOffline:
        text1 = "Open For Work"
        text2 = "I Am Working (deliverying)"
        text3 = "🟢 Go Offline"

    builder.add(InlineKeyboardButton(text=text1, callback_data="freeGuy", resize_keyboard=True, one_time_keyboard=True))
    builder.add(InlineKeyboardButton(text=text2, callback_data="WorkingGuy", resize_keyboard=True, one_time_keyboard=True))
    builder.row(InlineKeyboardButton(text="Search Job 🔎", callback_data="searchJob", resize_keyboard=True, one_time_keyboard=True))
    builder.row(InlineKeyboardButton(text=text3, callback_data="stopWorking", resize_keyboard=True, one_time_keyboard=True))
    builder.row(InlineKeyboardButton(text="My Profile", callback_data="triggerRelyProfile", resize_keyboard=True, one_time_keyboard=True))
    builder.add(InlineKeyboardButton(text="My Status", callback_data="myStatus", resize_keyboard=True, one_time_keyboard=True))
    builder.row(InlineKeyboardButton(text="Readme Instructions", callback_data="readMe", resize_keyboard=True, one_time_keyboard=True))
    inline_job_options = builder.as_markup()
    return inline_job_options

    
    
back_button_for_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Go Back", callback_data="callDeliveryMenu", resize_keyboar=True, one_time_keyboard=True)]
])
# inline_job_options = InlineKeyboardMarkup(inline_keyboard=[
#     [InlineKeyboardButton(text="I Am Free", callback_data="freeGuy")],
#     [InlineKeyboardButton(text="I Am Working (deliverying)", callback_data="WorkingGuy")]
# ],  resize_keyboard=True, one_time_keyboard=True)


# carts thing 
# show cart 
async def show_cart_inline(user_id, indicator):
    
    cart_items = await get_cart_items(user_id)
    builder = InlineKeyboardBuilder()
    cnt = 2
    for index,item in enumerate(cart_items):
        
        product_data = await get_product(item['product_id'])
        product_data = product_data[0]
        print('got product', product_data)
        if item['product_id'] == indicator:
            if cnt == 0:
                builder.row(
                    InlineKeyboardButton(text=f"🔘 {product_data['product_name']} (x{item['quantity']})", callback_data=f"view_cart_product|{product_data['product_id']}|{item['quantity']}", resize_keyboar=True, one_time_keyboard=True),
                )
                cnt = 2 
            else:
                builder.add(
                InlineKeyboardButton(text=f"🔘 {product_data['product_name']} (x{item['quantity']})", callback_data=f"view_cart_product|{product_data['product_id']}|{item['quantity']}", resize_keyboar=True, one_time_keyboard=True),
                
                )
                cnt -= 1 
        elif not indicator and index == 0:
            if cnt == 0:
                builder.row(
                    InlineKeyboardButton(text=f"🔘 {product_data['product_name']} (x{item['quantity']})", callback_data=f"view_cart_product|{product_data['product_id']}|{item['quantity']}", resize_keyboar=True, one_time_keyboard=True),
                )
                cnt = 2 
            else:
                builder.add(
                InlineKeyboardButton(text=f"🔘 {product_data['product_name']} (x{item['quantity']})", callback_data=f"view_cart_product|{product_data['product_id']}|{item['quantity']}", resize_keyboar=True, one_time_keyboard=True),
                
                )
                cnt -= 1 
        else:
            builder.row(
                InlineKeyboardButton(text=f"{product_data['product_name']} (x{item['quantity']})", callback_data=f"view_cart_product|{product_data['product_id']}|{item['quantity']}", resize_keyboar=True, one_time_keyboard=True),
            )

    builder.row(
        InlineKeyboardButton(text="Checkout Now 💳", callback_data="checkout_cart", resize_keyboar=True, one_time_keyboard=True)
    )
    builder.add(
        InlineKeyboardButton(text="Clear Cart Items 🗑", callback_data=f"empty_cart|{user_id}", resize_keyboar=True, one_time_keyboard=True)
    )
    return builder.as_markup()
    # print('showing cart items:', cart_items)
    