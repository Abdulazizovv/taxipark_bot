from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from bot.loader import dp, db
from bot.keyboards.default import phone_number_kb


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    
    await message.answer("Assalomu alaykum! \n"
                         "Botimizga xush kelibsiz!\n"
                         "Botdan foydalanish uchun telefon raqamingizni yuboring!", reply_markup=phone_number_kb)
    

@dp.message_handler(content_types=types.ContentType.CONTACT)
async def get_contact(message: types.Message):
    phone_number = message.contact.phone_number
    user_id = message.from_user.id
    
    # user ro'yxatdan o'tmagan bo'lsa, ro'yxatdan o'tkazamiz
    user = await db.get_or_create_user(
        user_id=user_id,
        phone_number=phone_number,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name
    )

    if user['created']:
        if user['user']['is_admin']:
            await message.answer("Siz admin sifatida ro'yxatdan o'tdingiz!\n"
                                 "/start buyrug'ini bering")
        elif user['user']['is_service']:
            await message.answer("Siz xizmat ko'rsatuvchi sifatida ro'yxatdan o'tdingiz!\n"
                                 "/start buyrug'ini bering")
        else:
            await message.answer("Siz muvaffaqiyatli ro'yxatdan o'tdingiz!\n"
                                 "Iltimos, hisobingiz aktivlashtirilishini kuting!")
    else:
        await message.answer("Siz avval ro'yxatdan o'tgansiz!\n"
                             "Iltimos, hisobingiz aktivlashtirilishini kuting!")




