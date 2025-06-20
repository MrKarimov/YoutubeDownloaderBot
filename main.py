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
from youtube import get_resolutions, download_video

# ⛳ TOKEN
TOKEN = os.getenv("BOT_TOKEN")

# 🧠 LOGGING (asosiy sozlama)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    stream=sys.stdout  # Terminalga chiqarish
)

logger = logging.getLogger(__name__)

# 🤖 Dispatcher
dp = Dispatcher()
user_links = {}  # user_id : youtube link

# 📥 Routerlar
dp.include_router(admin_router)
dp.include_router(user_router)

# 🔗 YouTube linkni qabul qilish
@dp.message(F.text.func(lambda text: "youtu" in text))
async def handle_youtube_link(message: Message):
    link = message.text
    user_id = message.from_user.id
    user_links[user_id] = link

    logger.info(f"📥 Link received from {user_id}: {link}")

    try:
        resolutions = get_resolutions(link)
    except Exception as e:
        logger.error(f"❌ Error getting resolutions for {link}: {e}", exc_info=True)
        await message.answer("❌ Linkni qayta ishlay olmadik.")
        return

    if not resolutions:
        await message.answer("❌ No quality found.")
        return

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=res, callback_data=res)] for res in resolutions
        ]
    )
    await message.answer("Which quality do you choose?", reply_markup=keyboard)

# 📥 Video yuklash va yuborish
@dp.callback_query()
async def handle_resolution(callback: CallbackQuery):
    resolution = callback.data
    user_id = callback.from_user.id
    link = user_links.get(user_id)

    logger.info(f"🎞 User {user_id} chose resolution: {resolution} for {link}")

    await callback.message.edit_text(f"⏳ {resolution} video is being prepared...")

    try:
        video_path = download_video(link, resolution)
        logger.info(f"✅ Video downloaded at: {video_path}")
    except Exception as e:
        logger.error(f"❌ Error downloading video ({link}) at {resolution}: {e}", exc_info=True)
        await callback.message.answer("❌ Video yuklab bo‘lmadi. Serverda xatolik yuz berdi.")
        return

    if video_path and os.path.exists(video_path):
        try:
            input_file = FSInputFile(path=video_path, filename=os.path.basename(video_path))
            await callback.message.answer_video(video=input_file, caption=f"🎬 {resolution} video")
        except Exception as e:
            logger.error(f"❌ Error while sending video to user {user_id}: {e}", exc_info=True)
            await callback.message.answer(f"❌ Error while sending: {e}")
        finally:
            os.remove(video_path)
            logger.info(f"🧹 Video file deleted: {video_path}")
    else:
        await callback.message.answer("❌ Failed to download the video. Please try again later.")

# 🚀 Botni ishga tushirish
async def main():
    await ensure_db_exists()
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    logger.info("🚀 Bot started polling...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
