from aiogram import types
from bot.loader import dp, db
from aiogram.dispatcher import FSMContext
from bot.filters import IsService
from bot.keyboards.default.service import select_service_category_keyboard


@dp.message_handler(IsService(), state="select_service_category")
async def select_service_category(message: types.Message, state: FSMContext):
    category = message.text
    
    # orqaga tugmasi bosilganda servis kategoriyasini tanlashga qaytadi
    if message.text == "⬅️ Orqaga":
        await message.answer("Xizmat kategoriyasini tanlang:", reply_markup=select_service_category_keyboard(await db.get_service_categories()))
        await state.set_state("select_service_category")
        return

    # tanlangan servis kategoriyasini bazadan olish
    service_category = await db.get_service_category_by_name(name=category)
    
    # agar servis kategoriyasi mavjud bo'lmasa ogohlantirish
    if not service_category.success:
        return await message.answer(service_category.message)
    
    await message.answer(f"Siz {service_category.data['name']} kategoriyasini tanladingiz.\n"
                         f"Haydovchini tanlang:", reply_markup=types.InlineKeyboardMarkup(
                             inline_keyboard=[
                                 [
                                     types.InlineKeyboardButton(text="Haydovchini tanlash", switch_inline_query_current_chat=""),
                                 ]
                             ]
                         ))

    await state.set_state("select_driver")
    await state.update_data(category_id=service_category.data['id'])    
