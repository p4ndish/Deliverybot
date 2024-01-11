import asyncio
import logging
import sys
from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from bot.bot_instance import bot
from bot.database.functions import start_db
from bot.handlers.welcome_handler import welcome_router
from bot.handlers.auth_handler import auth_router
from bot.handlers.shop_handler import shop_router
from bot.handlers.checkout_handler import checkout_router
from bot.handlers.delivery_guys_portal import delivery_router
from bot.handlers.cart_handler import cart_router



async def main():
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    
    await start_db()
    # include routers
    
    
    dp.include_router(welcome_router)
    dp.include_router(auth_router)  
    dp.include_router(delivery_router)  
    dp.include_router(shop_router)
    dp.include_router(checkout_router)
    dp.include_router(cart_router)
    
    
    dp._listen_updates(bot)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())