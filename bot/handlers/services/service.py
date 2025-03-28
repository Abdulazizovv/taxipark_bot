from aiogram import types
from bot.loader import dp, db
from aiogram.dispatcher import FSMContext
from bot.filters import IsService
from bot.keyboards.default.service import select_service_keyboard


@dp.message_handler(IsService(), text="📝 Xizmat ko'rsatish", state="*")
async def start_service(message: types.Message, state: FSMContext):
    await state.finish()
    services = await db.get_user_services(message.from_user.id)
    if not services.success:
        return await message.answer(services.message)
    services = services.data

    if not services:
        return await message.answer("Sizda xizmatlar mavjud emas")

    if len(services) == 1:
        await state.update_data(service_id=services[0]["id"])
        await message.answer("Xizmat tanlandi", reply_markup=types.ReplyKeyboardRemove())
        await message.answer(
            f"Xizmat nomi: {services[0]['title']}\n"
            f"Haydovchini tanlang",
            reply_markup=types.InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        types.InlineKeyboardButton(
                            text="Haydovchini tanlash",
                            switch_inline_query_current_chat="",
                        ),
                    ]
                ]
            ),
        )
        await state.set_state("select_driver")
        return

    await message.answer(
        "Xizmat ko'rsatish uchun tanlang",
        reply_markup=select_service_keyboard(services),
    )
    await state.set_state("select_service")
