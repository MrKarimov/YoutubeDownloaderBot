from aiogram import Router, types, F
from database.database import add_user # bu funksiya avval yozganing

user_router = Router()

@user_router.message(F.text == "/start")
async def start_handler(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.username or "no_username"
    full_name = message.from_user.full_name

    # Foydalanuvchini DBga qo‘shish (agar yo‘q bo‘lsa)
    await add_user(user_id, username, full_name)

    await message.answer(f"Hello, {full_name}! 👋\n\nWelcome to the YouTube Downloader Bot.\nSimply send a YouTube link below, and I’ll help you download it in your preferred quality. 🎥📥"
)



