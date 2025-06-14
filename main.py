import asyncio
import logging
import sys
import os

from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import FSInputFile, Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from database.database import ensure_db_exists
from admin import admin_router
from handlers import user_router
from dotenv import load_dotenv

from youtube import get_resolutions, download_video

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

dp = Dispatcher()
user_links = {}  # user_id : youtube link


dp.include_router(admin_router)
dp.include_router(user_router)



@dp.message(F.text.func(lambda text: "youtu" in text))
async def handle_youtube_link(message: Message):
    link = message.text
    user_id = message.from_user.id
    user_links[user_id] = link

    resolutions = get_resolutions(link)
    if not resolutions:
        await message.answer("❌ No quality found.")
        return

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=res, callback_data=res)] for res in resolutions
        ]
    )
    await message.answer("Which quality do you choose?", reply_markup=keyboard)


@dp.callback_query()
async def handle_resolution(callback: CallbackQuery):
    resolution = callback.data
    user_id = callback.from_user.id
    link = user_links.get(user_id)

    await callback.message.edit_text(f"⏳ {resolution} video is being prepared...")

    video_path = download_video(link, resolution)

    if video_path and os.path.exists(video_path):
        try:
            input_file = FSInputFile(path=video_path, filename=os.path.basename(video_path))
            await callback.message.answer_video(video=input_file, caption=f"🎬 {resolution} video")
        except Exception as e:
            await callback.message.answer(f"❌ Error while sending: {e}")
        finally:
            os.remove(video_path)
    else:
        await callback.message.answer("❌ Failed to download the video. Please try again later.")

async def main():
    await ensure_db_exists()
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
