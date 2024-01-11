# from aiogram import BaseMiddleware
# from aiogram.types import Message
# from typing import Dict, Any, Callable, Awaitable
# from aiogram.types import MenuButtonWebApp
# from aiogram.types.web_app_info import WebAppInfo
# import os
# from bot.database.functions import get_profile
# from bot.bot_instance import bot

# from dotenv import load_dotenv
# load_dotenv()

# class MenuMiddleware(BaseMiddleware):
#     def __init__(self) -> None:
#         self.menu = None

#     async def __call__(
#         self,
#         handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
#         event: Message,
#         data: Dict[str, Any]
#     ) -> Any:
#         print("middleware handler", event.from_user.id )
#         user_data = await get_profile(event.from_user.id)
#         if user_data:
            
#             # await bot.set_chat_menu_button(chat_id=event.from_user.id ,menu_button=MenuButtonWebApp(text="Profile", web_app=WebAppInfo(url=os.environ.get("APP_URL"))))

#         return await handler(event, data)