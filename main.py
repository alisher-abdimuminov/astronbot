import os
import sys
import dotenv
import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.client.default import DefaultBotProperties
from aiogram.types import Message, WebAppInfo, MenuButtonWebApp




async def send_message(bot: Bot, text: str):
    users = ""

    with open("users.txt", "r") as users_file:
        users = users_file.read().strip()

    for user in users.split("\n"):
        print("user", user)
        try:
            await bot.send_message(user, text)
            await asyncio.sleep(0.05)
        except Exception as e:
            print("Error: chat not found")
            users = users.replace(user, "")
    with open("users.txt", "w") as users_file:
        users_file.write(users)
    await bot.send_message(int(ADMIN), "Reklama foydalanuvchilarga yuborildi.")


dotenv.load_dotenv(".env")


TOKEN = os.getenv("TOKEN")
# TOKEN = "7854066706:AAGDV9_DgigT2QAe4zfNZjsly9hi4ECxt7c"
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

- Murojaat yo'llash uchun @astron_corp ga yozing.""")
    users = ""

    with open("users.txt", "r") as users_file:
        users = users_file.read().strip()
    
    if str(message.from_user.id) not in users:
        with open("users.txt", "a") as users_file:
            users_file.write("\n" + str(message.from_user.id) + "\n")


@dp.message(Command("stats"))
async def stats(message: Message) -> None:
    users = ""

    with open("users.txt", "r") as users_file:
        users = users_file.read().strip().split()
    await message.answer(f"Foydalanuvchilar soni: {len(users)}")


@dp.message()
async def any_message_handler(message: Message) -> None:
    if message.from_user.id == int(ADMIN):
        asyncio.create_task(send_message(bot, message.text))
    else:
        message.answer("- Murojaat yo'llash uchun @astron_corp ga yozing.")

    # else:
    #     await bot.send_message(chat_id=int(ADMIN), text=f"{message.from_user.first_name} {message.from_user.last_name if message.from_user.last_name else ''}\n{'t.me/' + message.from_user.username if message.from_user.username else ''}\n\n{message.text}\n{message.from_user.id}")


async def main() -> None:
    dp.startup.register(on_startup)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
