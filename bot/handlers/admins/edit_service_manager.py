from aiogram import types
from aiogram.dispatcher import FSMContext
from bot.keyboards.inline.service_manager_detail import service_manager_edit_kb
from bot.keyboards.inline.service_managers import select_manager_kb
from bot.loader import dp, db
from bot.keyboards.inline.edit_service_manager import manager_edit_callback
from bot.keyboards.inline.service_manager_detail import service_manager_edit_cb
from bot.keyboards.default import back_kb
from bot.utils.main import validate_phone_number
from bot.filters import IsAdmin



@dp.callback_query_handler(IsAdmin(), manager_edit_callback.filter(action="delete"), state="*")
async def delete_service_manager(
    call: types.CallbackQuery, callback_data: dict, state: FSMContext
):
    await state.finish()

    manager_id = callback_data.get("manager_id")
    service_id = callback_data.get("service_id")
    await state.update_data(manager_id=manager_id)
    await state.update_data(service_id=service_id)

    await call.message.answer("Servis xodimini o'chirishni tasdiqlaysizmi?", reply_markup=types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(text="Yo'q ✖️", callback_data="delete_employee:no"),
                types.InlineKeyboardButton(text="Ha ✅", callback_data="delete_employee:yes")
            ]
        ]
    ))


@dp.callback_query_handler(IsAdmin(), text="delete_employee:yes", state="*")
async def delete_service_manager_yes(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    manager_id = data.get("manager_id")
    service_id = data.get("service_id")

    db_response = await db.delete_service_manager(manager_id)
    if not db_response.success:
        return await call.message.answer(db_response.message)

    service = await db.get_service_by_id(service_id)
    if not service.success:
        return await call.message.answer(service.message)
    service = service.data

    managers = await db.get_service_managers(service_id)
    if not managers.success:
        return await call.message.answer(managers.message)
    managers = managers.data

    await state.finish()
    await call.message.edit_text("Menejer muvaffaqiyatli o'chirildi.\n"
                                 "Kerakli menejer tanlang yoki yangi menejer qo'shing.",
                                 reply_markup=select_manager_kb(managers, service_id))


@dp.callback_query_handler(IsAdmin(), manager_edit_callback.filter(action="edit"), state="*")
async def edit_service_manager(
    call: types.CallbackQuery, callback_data: dict, state: FSMContext
):
    await state.finish()

    manager_id = callback_data.get("manager_id")
    service_id = callback_data.get("service_id")

    manager = await db.get_service_manager(service_id, manager_id)
    if not manager.success:
        return await call.message.answer(manager.message)
    manager = manager.data

    await call.message.edit_text(f"Ism-familiya: {manager['full_name']}\n"
                                 f"Telefon raqam: {manager['phone_number']}\n\n"
                                 f"Nimani o'zgartiramiz?", reply_markup=service_manager_edit_kb(manager_id, service_id))
    await state.finish()



@dp.callback_query_handler(IsAdmin(), service_manager_edit_cb.filter(action="name"), state="*")
async def edit_service_manager_name(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await state.update_data(manager_id=callback_data.get("manager_id"))
    await state.update_data(service_id=callback_data.get("service_id"))
    await call.message.delete()
    await call.message.answer("Yangi ism-familiyani kiriting:", reply_markup=back_kb)
    await state.set_state("edit_service_manager_name")


@dp.message_handler(IsAdmin(), state="edit_service_manager_name")
async def edit_service_manager_name_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()
    manager_id = data.get("manager_id")
    service_id = data.get("service_id")

    if message.text == "◀️Orqaga":
        await state.finish()
        service = await db.get_service_by_id(service_id)
        if not service.success:
            return await message.answer(service.message)
        service = service.data

        managers = await db.get_service_managers(service_id)
        if not managers.success:
            return await message.answer(managers.message)
        managers = managers.data

        await message.answer("Kerakli menejer tanlang yoki yangi menejer qo'shing.",
                             reply_markup=select_manager_kb(managers, service_id))
        return


    db_response = await db.edit_service_manager_name(manager_id, message.text)
    if not db_response.success:
        return await message.answer(db_response.message)

    service = await db.get_service_by_id(service_id)
    if not service.success:
        return await message.answer(service.message)
    service = service.data

    managers = await db.get_service_managers(service_id)
    if not managers.success:
        return await message.answer(managers.message)
    managers = managers.data

    await state.finish()
    await message.answer("Menejer muvaffaqiyatli o'zgartirildi.\n"
                         "Kerakli menejer tanlang yoki yangi menejer qo'shing.",
                         reply_markup=select_manager_kb(managers, service_id))


@dp.callback_query_handler(IsAdmin(), service_manager_edit_cb.filter(action="phone_number"), state="*")
async def edit_service_manager_phone_number(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await state.update_data(manager_id=callback_data.get("manager_id"))
    await state.update_data(service_id=callback_data.get("service_id"))
    await call.message.delete()
    await call.message.answer("Yangi telefon raqamni kiriting:", reply_markup=back_kb)
    await state.set_state("edit_service_manager_phone_number")


@dp.message_handler(IsAdmin(), state="edit_service_manager_phone_number")
async def edit_service_manager_phone_number_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()
    manager_id = data.get("manager_id")
    service_id = data.get("service_id")

    if message.text == "◀️Orqaga":
        await message.answer("Yangi telefon raqamni kiriting:", reply_markup=back_kb)
        await state.set_state("edit_service_manager_phone_number")
        return
    
    if not validate_phone_number(message.text):
        return await message.answer("Noto'g'ri telefon raqam kiritildi. Iltimos, qaytadan urinib ko'ring.\n"
                                    "Masalan: +998901234567")

    db_response = await db.edit_service_manager_phone_number(manager_id, message.text)
    if not db_response.success:
        return await message.answer(db_response.message)

    service = await db.get_service_by_id(service_id)
    if not service.success:
        return await message.answer(service.message)
    service = service.data

    managers = await db.get_service_managers(service_id)
    if not managers.success:
        return await message.answer(managers.message)
    managers = managers.data

    await state.finish()
    await message.answer("Menejer muvaffaqiyatli o'zgartirildi.\n"
                         "Kerakli menejer tanlang yoki yangi menejer qo'shing.",
                         reply_markup=select_manager_kb(managers, service_id))


@dp.callback_query_handler(IsAdmin(), service_manager_edit_cb.filter(action="back"), state="*")
async def back_to_service_managers(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await state.finish()

    service_id = callback_data.get("service_id")

    service = await db.get_service_by_id(service_id)
    if not service.success:
        return await call.message.answer(service.message)
    service = service.data

    managers = await db.get_service_managers(service_id)
    if not managers.success:
        return await call.message.answer(managers.message)
    managers = managers.data

    await call.message.edit_text("Kerakli menejer tanlang yoki yangi menejer qo'shing.",
                                 reply_markup=select_manager_kb(managers, service_id))