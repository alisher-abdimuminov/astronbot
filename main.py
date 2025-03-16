import sys
import asyncio
import logging
import os
import dotenv
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo, MenuButtonWebApp


dotenv.load_dotenv()


TOKEN = os.getenv("TOKEN")
ADMIN = os.getenv("ADMIN")
print(ADMIN)


dp = Dispatcher()
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))



async def on_startup(bot: Bot):
    print("set menu button")
    await bot.set_chat_menu_button(
        menu_button=MenuButtonWebApp(text="Ilovani ochish", web_app=WebAppInfo(url=f"https://astron-web-app.vercel.app"))
    )

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer("""Assalomu aleykum.

"ASTRON - onlayn repetitor" loyihasining ilovasiga xush kelibsiz!!!

- Ilovadan foydalanish uchun pastgi chap burchakdagi "Ilovani ochish" tugmasiga bosing.

- Murojaat yo'llash uchun ushbu botga yozing.""")


@dp.message()
async def any_message_handler(message: Message) -> None:
    if message.from_user.id == int(ADMIN):
        if (message.reply_to_message):
            await bot.send_message(message.reply_to_message.forward_from.id, message.text)
    else:
        await bot.forward_message(chat_id=int(ADMIN), from_chat_id=message.from_user.id, message_id=message.message_id)


async def main() -> None:
    dp.startup.register(on_startup)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
