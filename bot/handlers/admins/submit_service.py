from aiogram import types
from bot.loader import dp, db
from aiogram.dispatcher import FSMContext
from bot.keyboards.inline.submit_service import submit_service_cb
from bot.keyboards.inline.service_edit import service_edit_kb
from bot.keyboards.default import admin_menu_kb


@dp.callback_query_handler(submit_service_cb.filter(action="submit"), state="*")
async def submit_service(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    data = await state.get_data()

    db_response = await db.create_new_service(
        title=data.get("service_name"),
        description=data.get("service_description"),
        phone_number=data.get("service_phone"),
        user_id=call.from_user.id
    )

    if not db_response.success:
        await call.message.edit_reply_markup()
        await call.message.answer(db_response.message)
        return
    
    service_id = db_response.data['service_id']

    service_response = await db.get_service_by_id(service_id)
    if not service_response.success:
        await call.message.answer(service_response.message)
        return
    
    service = service_response.data
    await call.message.delete()

    await call.message.answer(
        "Yangi servis yaratildi!✅\n\n"
        f"<b>🆔 ID:</b> {service['id']}\n"
        f"<b>🔧 Servis nomi:</b> {service['title']}\n"
        f"<b>📋 Ma'lumot:</b> {service['description']}\n"
        f"<b>📞 Telefon raqam:</b> {service['phone_number']}\n"
        f"<b>📅 Yaratilgan vaqti:</b> {service['created_at'].strftime("%d-%m-%Y %H:%M")}\n",
        reply_markup=service_edit_kb(service['id'])
    )


@dp.callback_query_handler(submit_service_cb.filter(action="cancel"), state="*")
async def cancel_service(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.edit_reply_markup()
    await call.message.answer("Servis yaratish bekor qilindi!❌\n"
                              "Bosh menyuga qatdingiz.", reply_markup=admin_menu_kb)