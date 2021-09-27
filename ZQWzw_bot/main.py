from aiogram import types, Bot, Dispatcher, executor
import secrets
import os, sys
import io
import aiohttp
import boty

bot = Bot(token=boty.ZQWzw_bot)
dp = Dispatcher(bot)
@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.answer(
        f"🔱 Привет, {(message.from_user.first_name)}!🔱 Я Бот Фотохостинг ! "
        f"⚠️Используй только меня, остерегайся фэйков!⚠️ \n\n"
        f"🔱Просто отправь мне фотографию. Также, ее можно отправить документом.🔱"
    )
@dp.message_handler(content_types=["photo"])
async def download_photo(message: types.Message):
    password = secrets.token_urlsafe(5)
    await message.photo[-1].download(destination=f"{password}.jpg")
    with io.open(f'{password}.jpg', 'rb') as file:
        form = aiohttp.FormData()
        form.add_field(
            name="file",
            value=file,
        )
        async with bot.session.post("https://telegra.ph/upload", data=form) as response:
            img_src = await response.json()
    link = ("http://telegra.ph/" + img_src[0]["src"])
    with open(f'{password}.jpg', 'rb') as photo:
        await message.reply(f"✓ Изображение загружено \n{link}",
        disable_web_page_preview=True)
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), f"{password}.jpg")
    os.remove(path)

        
if __name__ == "__main__":
    executor.start_polling(dp)