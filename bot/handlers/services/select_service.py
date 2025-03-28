from aiogram import types
from bot.loader import dp, db
from aiogram.dispatcher import FSMContext
from bot.filters import IsService
from bot.keyboards.default.service import select_service_category_keyboard
from bot.keyboards.default import service_admin_menu_kb
from bot.keyboards.default import back_kb


@dp.message_handler(IsService(), state="select_service")
async def select_service(message: types.Message, state: FSMContext):

    if message.text == "🔙 Orqaga":
        await state.finish()

        return await message.answer(
            "Bosh menyu qaytdingiz", reply_markup=service_admin_menu_kb
        )

    service = await db.get_service_by_title(message.text)
    if not service.success:
        return await message.answer(service.message)
    service = service.data
    await state.update_data(service_id=service["id"])
    await message.answer("Xizmat tanlandi", reply_markup=back_kb)
    await message.answer(
        
        f"Xizmat nomi: {service['title']}\n" f"Haydovchini tanlang",
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
