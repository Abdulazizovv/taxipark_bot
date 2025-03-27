from aiogram import types
from bot.loader import dp, db
from aiogram.dispatcher import FSMContext
from bot.keyboards.inline import service_edit_kb
from bot.keyboards.default import admin_menu_kb
from bot.filters import IsAdmin


@dp.message_handler(IsAdmin(), content_types=types.ContentTypes.TEXT, state="select_service")
async def get_selected_service(message: types.Message, state: FSMContext):
    selected_service = message.text
    if message.text == "⬅️Orqaga":
        await state.finish()
        await message.answer("Bosh menyuga qaytdingiz.", reply_markup=admin_menu_kb)
        return

    await state.update_data(selected_service=selected_service)

    selected_service_data = await db.get_service_by_title(selected_service)
    if not selected_service_data.success:
        await message.answer("Bunday servis topilmadi")
        return
    
    selected_service = selected_service_data.data
    await message.answer(
        f"<b>🆔 ID:</b> {selected_service['id']}\n"
        f"<b>🔧 Servis nomi:</b> {selected_service['title']}\n"
        f"<b>📋 Ma'lumot:</b> {selected_service['description'] if selected_service['description'] else '<i>Mavjud emas</i>'}\n"
        f"<b>📞 Telefon raqam:</b> {selected_service['phone_number']}\n"
        f"<b>⚙️ Kategoriyalari:</b> {', '.join([category for category in selected_service['categories']])}\n"
        f"<b>📅 Yaratilgan vaqti:</b> {selected_service['created_at'].strftime("%d-%m-%Y %H:%M")}\n",
        reply_markup=service_edit_kb(selected_service['id'])
    )