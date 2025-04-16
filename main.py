import sys
import asyncio
import logging
import os
import dotenv
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram import Bot, Dispatcher, html
from threading import Thread
from aiogram.client.default import DefaultBotProperties
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo, MenuButtonWebApp




async def send_message(bot: Bot, text: str):
    try:
        users = ""

        with open("users.txt", "r") as users_file:
            users = users_file.read()

        for user in users:
            bot.send_message(user, text)
    except Exception as e:
        print(e)


class Worker(Thread):
    def __init__(self, bot: Bot, text: str):
        self.bot = bot
        self.text = text
        super().__init__()

    async def run(self):
        await send_message(self.bot, self.text)


dotenv.load_dotenv(".env")


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
            user_id = message.reply_to_message.text.split("\n")[-1]
            await bot.send_message(user_id, message.text)
    else:
        if message.text == "send":
            worker = Worker(bot, "Salom")
            worker.start()
        await bot.send_message(chat_id=int(ADMIN), text=f"{message.from_user.first_name} {message.from_user.last_name if message.from_user.last_name else ''}\n{'t.me/' + message.from_user.username if message.from_user.username else ''}\n\n{message.text}\n{message.from_user.id}")


async def main() -> None:
    dp.startup.register(on_startup)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
