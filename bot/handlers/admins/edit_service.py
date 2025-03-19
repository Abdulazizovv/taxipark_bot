from aiogram import types
from aiogram.dispatcher import FSMContext
from bot.loader import dp, db
from bot.keyboards.inline import service_edit_callback
from bot.keyboards.inline.edit_service_section import edit_service_section_kb, edit_service_section_cb
from bot.keyboards.default import admin_menu_kb


@dp.callback_query_handler(service_edit_callback.filter(action="delete"), state="*")
async def delete_service(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await state.finish()

    service_id = callback_data.get("service_id")
    db_response = await db.delete_service(service_id)
    if not db_response.success:
        return await call.message.answer(db_response.message)

    await call.message.edit_reply_markup()
    await call.message.answer("Servis muvaffaqiyatli o'chirildi.", reply_markup=admin_menu_kb)


@dp.callback_query_handler(service_edit_callback.filter(action="edit"), state="*")
async def edit_service(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await state.finish()

    service_id = callback_data.get("service_id")
    service = await db.get_service_by_id(service_id)

    if not service.success:
        return await call.message.answer(service.message)
    
    service = service.data

    await call.message.edit_text(
        f"Servisni tahrirlash:\n\n"
        f"Servis nomi: {service['title']}\n"
        f"Servis haqida: {service['description']}\n"
        f"Telefon raqam: {service['phone_number']}\n"
        f"Kategoriya: {', '.join(service['categories'])}\n\n"
        f"Nimani o'zgartiramiz?",
        reply_markup=edit_service_section_kb(service_id=service_id)
    )


@dp.callback_query_handler(edit_service_section_cb.filter(section="name"))
async def edit_service_name(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await call.message.edit_text("Servis nomini kiriting:")
    await state.set_state("edit_service_name")
    await state.update_data(service_id=callback_data.get("service_id"))


@dp.message_handler(state="edit_service_name")
async def get_service_name(message: types.Message, state: FSMContext):
    data = await state.get_data()
    service_name = message.text
    db_response = await db.edit_service_title(service_id=data.get("service_id"), title=service_name)
    if not db_response.success:
        await message.answer(db_response.message)
        return

    await message.answer("Servis nomi muvaffaqiyatli o'zgartirildi.")
    await state.finish()


@dp.callback_query_handler(edit_service_section_cb.filter(section="description"))
async def edit_service_description(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await call.message.edit_text("Servis haqida ma'lumot kiriting:")
    await state.set_state("edit_service_description")
    await state.update_data(service_id=callback_data.get("service_id"))


@dp.message_handler(state="edit_service_description")
async def get_service_description(message: types.Message, state: FSMContext):
    data = await state.get_data()
    service_description = message.text
    db_response = await db.edit_service_description(service_id=data.get("service_id"), description=service_description)
    if not db_response.success:
        await message.answer(db_response.message)
        return

    await message.answer("Servis haqida ma'lumot muvaffaqiyatli o'zgartirildi.")
    await state.finish()


@dp.callback_query_handler(edit_service_section_cb.filter(section="phone"))
async def edit_service_phone(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await call.message.edit_text("Telefon raqamni kiriting:")
    await state.set_state("edit_service_phone")
    await state.update_data(service_id=callback_data.get("service_id"))


@dp.message_handler(state="edit_service_phone")
async def get_service_phone(message: types.Message, state: FSMContext):
    data = await state.get_data()
    phone_number = message.text
    db_response = await db.edit_service_phone_number(service_id=data.get("service_id"), phone_number=phone_number)
    if not db_response.success:
        await message.answer(db_response.message)
        return

    await message.answer("Telefon raqam muvaffaqiyatli o'zgartirildi.")
    await state.finish()

