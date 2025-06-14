
from aiogram.types import ReplyKeyboardRemove
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram import Router, types, F,Bot
from database.database import user_info,  user_full_info, get_all_user_ids
import os
import csv
from aiogram.types import FSInputFile

ADMIN = int(os.getenv("ADMIN"))
admin_router = Router()
@admin_router.message(F.from_user.id == ADMIN, F.text == "/admin")
async def admin_panel(message: types.Message):
    kb = [
        [types.KeyboardButton(text="👥 Users")],
        [types.KeyboardButton(text="📠Create CSV")],
        [types.KeyboardButton(text="📢 Send Ads")],
    ]
    markup = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer("👮‍♂️ Welcome!", reply_markup=markup)


@admin_router.message(F.from_user.id== ADMIN, F.text == "👥 Users")
async def show_users(message: types.Message):
    users = await user_info()
    if users:
        text = "\n".join([f"{u[0]} | {u[1]} | {u[2]}" for u in users])
    else:
        text = "Foydalanuvchilar yo‘q."
    await message.answer(text)

@admin_router.message(F.from_user.id == ADMIN, F.text == "📠Create CSV")
async def create_csv_file(message: types.Message):
    users = await user_full_info()
    
    if not users:
        await message.answer("❌ Ma'lumotlar topilmadi.")
        return

    filename = "users.csv"
    # CSV faylga yozish
    with open(filename, "w", newline='', encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["User ID", "Username", "Full Name", "Joined At"])  # sarlavha
        for user in users:
            writer.writerow(user)

    
    file = FSInputFile(filename)
    await message.answer_document(file, caption="📄 Foydalanuvchilar CSV fayli")

   
    os.remove(filename)




class BroadcastState(StatesGroup):
    waiting_for_message = State()


@admin_router.message(F.from_user.id == ADMIN, F.text == "📢 Send Ads")
async def start_broadcast(message: types.Message, state: FSMContext):
    await message.answer("📨 Reklama matnini yuboring:", reply_markup=ReplyKeyboardRemove())
    await state.set_state(BroadcastState.waiting_for_message)


@admin_router.message(BroadcastState.waiting_for_message)
async def do_broadcast(message: types.Message, state: FSMContext, bot: Bot):
    user_ids = await get_all_user_ids()
    success = 0
    failed = 0

    # Tekshiramiz: rasm bormi?
    if message.photo:
        photo = message.photo[-1].file_id  # eng yuqori sifatli rasm
        caption = message.caption or ""  # rasm ostidagi matn
        for uid in user_ids:
            try:
                await bot.send_photo(chat_id=uid, photo=photo, caption=caption)
                success += 1
            except Exception:
                failed += 1
    else:
        # faqat matn
        for uid in user_ids:
            try:
                await bot.send_message(chat_id=uid, text=message.text)
                success += 1
            except Exception:
                failed += 1

    await message.answer(f"📢 Yuborildi: {success} ta\n🚫 Yuborilmadi: {failed} ta")
    await state.clear()