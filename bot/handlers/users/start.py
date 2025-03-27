from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from bot.loader import dp, db
from bot.keyboards.default import phone_number_kb


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    user = await db.get_or_create_bot_user(
        user_id=message.from_user.id,
        full_name=message.from_user.full_name,
        username=message.from_user.username,
    )
    print("start", user)

    await message.answer(
        "Assalomu alaykum! Botimizga xush kelibsiz!\n"
        "Hisobingizga kirish uchun telefon raqamingizni yuboring👇",
        reply_markup=phone_number_kb,
    )


@dp.message_handler(content_types=types.ContentType.CONTACT)
async def get_contact(message: types.Message):
    phone_number = message.contact.phone_number
    print(phone_number)
    response = await db.connect_user_to_employee(
        user_id=message.from_user.id, phone_number=phone_number
    )
    if response:
        await message.answer(
            "Siz tizimga kirdingiz!\n"
            "/start buyrug'ini bosing va bosh menyuga qayting!",
            reply_markup=types.ReplyKeyboardRemove(),
        )
    else:
        await message.answer(
            "Bu raqamga ega bo'lgan hodim topilmadi! Iltimos, qaytadan urinib ko'ring!"
        )
