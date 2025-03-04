import sys
import asyncio
import logging
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo, MenuButtonWebApp

TOKEN = "8157851127:AAE3OnIrHiggFB5r3V9r6qIBJ0fOTo2PHxQ"


dp = Dispatcher()


async def on_startup(bot: Bot):
    print("set menu button")
    await bot.set_chat_menu_button(
        menu_button=MenuButtonWebApp(text="Ilovani ochish", web_app=WebAppInfo(url=f"https://astron-web-app.vercel.app"))
    )

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Ilovani ochish",
                    web_app=WebAppInfo(url=f'https://astron-web-app.vercel.app'),
                )
            ]
        ]
    )
    await message.answer(f"\"ASTRON - onlayn repetitor\" loyihasining Telegramdagi ilovasi.", reply_markup=markup)


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp.startup.register(on_startup)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
