import asyncio
import os
import time
import uuid
from aiogram import types, Router, F
from aiogram.types import ShippingOption
from bot.bot_instance import bot
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
from bot.keyboards import inline_keyboards
from bot.utils.backend_request import add_delivery_person_to_orders, add_to_cart, check_if_not_exist, create_order, delete_user_cart, fetch_who_accepts, find_delivery_guy, get_cart_items, get_delivery_profile, get_product, move_product_to_orders_detail, move_user_cart_to_order_details
from bot.utils.image_compressor import combine_images_from_urls
from bot.utils.shared_functions import send_inline_providers
from bot.utils.states import Checkout
checkout_router = Router()
PAYMENTS_PROVIDER_TOKEN= os.environ.get('PAYMENTS_PROVIDER_TOKEN')
BASE_URL = os.environ.get('APP_URL')


# # Setup shipping options
# shipping_options = [
#     types.ShippingOption(id='instant', title='WorldWide Teleporter', prices=prices),
#     types.ShippingOption(id='pickup', title='Local pickup', prices=prices)
# ]


@checkout_router.message(Command('starti'))
async def cmd_start(message: types.Message):
    
    await bot.send_message(message.chat.id,
                           "Hello, I'm the demo merchant message."
                           " I can sell you a Time Machine."
                           " Use /buy to order one, /terms for Terms and Conditions")


@checkout_router.message(Command('terms'))
async def cmd_terms(message: types.Message):
    await bot.send_message(message.chat.id,
                           'Thank you for shopping with our demo message. We hope you like your new time machine!\n'
                           '1. If your time machine was not delivered on time, please rethink your concept of time'
                           ' and try again.\n'
                           '2. If you find that your time machine is not working, kindly contact our future service'
                           ' workshops on Trappist-1e. They will be accessible anywhere between'
                           ' May 2075 and November 4000 C.E.\n'
                           '3. If you would like a refund, kindly apply for one yesterday and we will have sent it'
                           ' to you immediately.')

@checkout_router.callback_query(lambda c: c.data == 'cancel_checkout_inline')
async def cancel_checkout_inline_handler(call: CallbackQuery):
    await call.message.delete()
    await send_inline_providers(call, FSMContext)

@checkout_router.callback_query(lambda c: c.data.startswith('checkout_now') )
async def cmd_buy(call: CallbackQuery, state: FSMContext):
    _, product_id, current_piece = call.data.split("|")

    product_data = await get_product(product_id)
    product_data = product_data[0]
    amount = int(product_data['product_price']) * int(current_piece)
    print(amount, product_data['product_price'], current_piece)
    prices = [
        types.LabeledPrice(label='Food Fee', amount=amount*100),
        types.LabeledPrice(label='Delivery Fee', amount=5000)
    ]

    # await bot.send_message(call.message.chat.id,
    #                        "Real cards won't work with me, no money will be debited from your account."
    #                        " Use this test card number to pay for your Time Machine: `4242 4242 4242 4242`"
    #                        "\n\nThis is your demo invoice:", parse_mode='Markdown')
    await state.set_state(Checkout.directly)
    await state.update_data(product_id=product_id)
    await state.update_data(quantity=current_piece)
    await bot.send_invoice(call.message.chat.id, title='Zergaw Payment Invoice',
                       description='We are making your payment as easy as possible\n'
                                   ' Please Continue on the payment process \n'
                                   ' You are buying: \n'
                                   f'{product_data["product_name"]} \n'
                                   f'{product_data["product_description"]}',
                       provider_token=PAYMENTS_PROVIDER_TOKEN,
                       currency='ETB',
                       photo_url=os.environ.get('APP_URL') + '/images/' + product_data['product_image_url'],
                       photo_height=512,
                       photo_width=512,
                       photo_size=512,
                       is_flexible=False,
                       prices=prices,
                       start_parameter='time-machine-example',
                       payload='HAPPY FRIDAYS COUPON', 
                       #reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Cancel", callback_data="sdf")]],resize_keyboard=True,one_time_keyboard=True)
                       )

@checkout_router.callback_query(lambda c: c.data.startswith('checkout_cart') )
async def cmd_buy(call: CallbackQuery, state: FSMContext ):
    await bot.send_chat_action(chat_id=call.from_user.id, action='upload_document')
    # get the cart items 
    # from the product find the product id 
    # caclucate the prices
    # list them  in prices table
    food_fee = 0
    carts = await get_cart_items(call.from_user.id)
    image_urls = []
    for item in carts:
        await bot.send_chat_action(chat_id=call.from_user.id, action='upload_document')
        pr = await get_product(item['product_id'])
        pr= pr[0]
        food_fee += pr['product_price'] * item['quantity']
        image_urls.append(BASE_URL + '/images/' + pr['product_image_url'])
    print('total fee, ', food_fee)
    prices = [
        types.LabeledPrice(label='Food Fee', amount=food_fee*100),
        types.LabeledPrice(label='Delivery Fee', amount=5000)
    ]
    height, width = combine_images_from_urls(image_urls)
    path = "bot/medias/checkout_cart.jpg"
    photo = open(path, 'rb').read()
    
    checkout_media = types.BufferedInputFile(photo,filename=f"chekoutimg.png")
    checkout_media = BASE_URL + '/images/logo/checkout_cart.jpg'
    # await bot.send_message(call.message.chat.id,
    #                        "Real cards won't work with me, no money will be debited from your account."
    #                        " Use this test card number to pay for your Time Machine: `4242 4242 4242 4242`"
    #                        "\n\nThis is your demo invoice:", parse_mode='Markdown')
    await state.set_state(Checkout.from_cart)
    await bot.send_invoice(call.message.chat.id, title='Zergaw Payment Invoice',
                       description='We are making your payment as easy as possible\n'
                                   ' Please Continue on the payment process \n'
                                   '\n',
                       provider_token=PAYMENTS_PROVIDER_TOKEN,
                       currency='ETB',
                       photo_url=checkout_media,
                       photo_height=height,
                       photo_width=width,
                       photo_size=height*width,
                       is_flexible=False,
                       prices=prices,
                       start_parameter='zergaw_delivery_payment',
                       payload='HAPPY FRIDAYS COUPON', 
                       #reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Cancel", callback_data="sdf")]],resize_keyboard=True,one_time_keyboard=True)
                       )



# @checkout_router.shipping_query(lambda query: True)
# async def shipping(shipping_query: typ es.ShippingQuery):
#     await bot.answer_shipping_query(shipping_query.id, ok=True, shipping_options=shipping_options,
#                                     error_message='Oh, seems like our Dog couriers are having a lunch right now.'
#                                                   ' Try again later!')


@checkout_router.pre_checkout_query(lambda query: True)
async def checkout(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True,
                                        error_message="Aliens tried to steal your card's CVV,"
                                                      " but we successfully protected your credentials,"
                                                      " try to pay again in a few minutes, we need a small rest.")


@checkout_router.message(F.successful_payment, Checkout.directly)
async def got_payment(message: types.Message, state: FSMContext):
    state_data = await state.get_data()
    if not state_data:
        await message.answer("Something went wrong Please, /start again")
        return 
    product_id = state_data['product_id']
    quantity = state_data['quantity']
    order_id_uuid = str(uuid.uuid4())
    data = {'order_id': order_id_uuid, 'customer_id': message.from_user.id }
    stat = await create_order(data)
    await message.answer(text=f"Order was successfully created.\nhere is your order ID, #{order_id_uuid} \n finding you delivery person...🔎")
    # move item to orders detail 
    stat = await move_product_to_orders_detail(product_id, quantity, order_id_uuid)
    print("status of moving product to orders detail: " , stat)
    if not stat:
        stat = await move_product_to_orders_detail(product_id, quantity, order_id_uuid)
        print("status of moving product to orders detail: " , stat)

    status_of_delivery = await find_delivery_guy()
    # find delivery guy
    while not status_of_delivery:
        await asyncio.sleep(2)
        status_of_delivery =  await find_delivery_guy()
    # if status_of_delivery:

    #     print("found delivery person: ", status_of_delivery)
    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        InlineKeyboardButton(text="Accept Order", callback_data=f"accept_order|{order_id_uuid}", )
    )
    keyboard.add(
        InlineKeyboardButton(text="Decline Order", callback_data=f"decline_order|{order_id_uuid}")
    )
    for delivery_person in status_of_delivery:
        UserId = delivery_person['user_id']
        stat = await add_delivery_person_to_orders(UserId, order_id_uuid)
        print("printing add_delivery_person_to_orders: ", stat)
        await bot.send_message(chat_id=UserId, text="you want a job or not?", reply_markup=keyboard.as_markup(),)
    

    who_accepts = await fetch_who_accepts(order_id_uuid)
    print("found who accepts: ", who_accepts)
    while not who_accepts :
        await asyncio.sleep(2)
        who_accepts = await fetch_who_accepts(order_id_uuid)
    
    delivery_person_detail = await get_delivery_profile(who_accepts[0]['delivery_guy_id'])
    dp = delivery_person_detail[0]
    print("got delivery_person_detail: ", delivery_person_detail)
    msg = f"""<b>✅Delivery person Found.\n👤<u>Here is information about your delivery person:</u>\n
    ➖ First Name: {dp['firstName']}
    ➖ Last Name: {dp['lastName']}
    ➖ Phone Number: {dp['phoneNumber']}

    ⚠️The Person will call you in a minute please confirm your location to the person. </b>
    """
    await message.answer_photo(photo=dp['photoURL'], caption=msg, parse_mode='HTML')
    
    await message.answer("After you order has been delivered, make sure you click on `order completed`", reply_markup=inline_keyboards.order_completed(dp['user_id']))



    

@checkout_router.message(F.successful_payment, Checkout.from_cart)
async def got_payment(message: types.Message):
    # print success message 
    # empty user cart 
    # initailize order 
    # wait until delivery guy is found

    
    print("message handler received in cart checkout: ", message.from_user.id)
    special_characters = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
    escape_table = str.maketrans({char: f'\\{char}' for char in special_characters})
    # msg = 'Hoooooray! Thanks for payment! We will proceed your order for `{} {}` as fast as possible! Stay in touch. \n\nUse /buy again to get a Time Machine for your friend!'.format(message.successful_payment.total_amount / 100, message.successful_payment.currency)
    # msg = msg.translate(escape_table)
    # await message.answer(text=msg, parse_mode='MarkdownV2')

    # await delete_user_cart(message.from_user.id)
    # CREATE order id 
    order_id_uuid = str(uuid.uuid4())
    data = {'order_id': order_id_uuid, 'customer_id': message.from_user.id }
    stat = await create_order(data)
    await message.answer(text=f"Order was successfully created. here is your order ID, #{order_id_uuid} \n finding you delivery person...🔎")

    move_stat = await move_user_cart_to_order_details(message.from_user.id, order_id_uuid)
    print(move_stat)
    # find free delivery person 
    # send them accept or reject request 
    # fetch timely on orders table to get the delivery person who accepts it 
    
    # await check_if_not_exist(order_id_uuid)
    status_of_delivery = await find_delivery_guy()
    # find delivery guy
    while not status_of_delivery:
        await asyncio.sleep(2)
        status_of_delivery =  await find_delivery_guy()
    # if status_of_delivery:

    #     print("found delivery person: ", status_of_delivery)
    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        InlineKeyboardButton(text="Accept Order", callback_data=f"accept_order|{order_id_uuid}", )
    )
    keyboard.add(
        InlineKeyboardButton(text="Decline Order", callback_data=f"decline_order|{order_id_uuid}")
    )
    for delivery_person in status_of_delivery:
        UserId = delivery_person['user_id']
        stat = await add_delivery_person_to_orders(UserId, order_id_uuid)
        print("printing add_delivery_person_to_orders: ", stat)
        await bot.send_message(chat_id=UserId, text="you want a job or not?", reply_markup=keyboard.as_markup(),)
    

    who_accepts = await fetch_who_accepts(order_id_uuid)
    print("found who accepts: ", who_accepts)
    while not who_accepts :
        await asyncio.sleep(2)
        who_accepts = await fetch_who_accepts(order_id_uuid)
    
    delivery_person_detail = await get_delivery_profile(who_accepts[0]['delivery_guy_id'])
    dp = delivery_person_detail[0]
    print("got delivery_person_detail: ", delivery_person_detail)
    msg = f"""<b>✅Delivery person Found.\n👤<u>Here is information about your delivery person:</u>\n
    ➖ First Name: {dp['firstName']}
    ➖ Last Name: {dp['lastName']}
    ➖ Phone Number: {dp['phoneNumber']} """
    await message.answer_photo(photo=dp['photoURL'], caption=msg, parse_mode='HTML')
    
    await message.answer("After you order has been delivered, make sure you click on `order completed`", reply_markup=inline_keyboards.order_completed(dp['user_id']))




@checkout_router.callback_query(lambda c: c.data.startswith('order_completed_inline') )
async def succes_delivery(call: CallbackQuery, state: FSMContext ):
    _, user_id = call.data.split('|')
    await call.message.answer(text="Thanks for the Confirmation.🙏, have a nice day", reply_markup=inline_keyboards.rate_user(user_id))


@checkout_router.callback_query(lambda c: c.data.startswith('rated_user') )
async def rated_user_send_message(call: CallbackQuery, state: FSMContext, ):
    _, user_id = call.data.split("|")
    await bot.send_message(chat_id=user_id, text="🙌 Good job on completing your job successfully!", )