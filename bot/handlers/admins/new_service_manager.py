from aiogram import types
from bot.keyboards.inline.edit_service_manager import manager_edit_kb
from bot.keyboards.inline.service_edit import service_edit_kb
from bot.loader import dp, db
from aiogram.dispatcher import FSMContext
from bot.keyboards.inline.service_managers import (
    select_manager_callback,
    select_manager_kb,
)
from bot.keyboards.default import back_kb as back
from bot.utils.main import validate_phone_number
from bot.filters import IsAdmin


@dp.callback_query_handler(IsAdmin(), select_manager_callback.filter(), state="*")
async def select_manager(
    call: types.CallbackQuery, callback_data: dict, state: FSMContext
):
    manager_id = callback_data.get("manager_id")
    service_id = callback_data.get("service_id")
    await state.update_data(manager_id=manager_id)
    await state.update_data(service_id=service_id)
    manager_id = int(manager_id)
    print(manager_id, service_id)

    if manager_id == 0:
        await call.message.delete()
        await call.message.answer("Yangi menejer ismini kiriting:", reply_markup=back)
        await state.set_state("new_manager_name")
        return

    if manager_id == -1:
        service = await db.get_service_by_id(service_id)
        if not service.success:
            return await call.message.answer(service.message)
        service = service.data

        await call.message.edit_text(
            f"Servisni tahrirlash:\n\n"
            f"Servis nomi: {service['title']}\n"
            f"Servis haqida: {service['description']}\n"
            f"Telefon raqam: {service['phone_number']}\n\n"
            f"Nimani o'zgartiramiz?",
            reply_markup=service_edit_kb(service_id),
        )
        return

    db_response = await db.get_service_manager(service_id, manager_id)
    if not db_response.success:
        return await call.message.answer(db_response.message)

    manager = db_response.data

    await call.message.edit_text(
        "Xizmat ko'rsatuvchi menejer ma'lumotlari:\n"
        f"Ismi: {manager['full_name']}\n"
        f"Telefon raqami: {manager['phone_number']}",
        reply_markup=manager_edit_kb(manager_id, service_id),
    )


@dp.message_handler(IsAdmin(), state="new_manager_name")
async def new_manager_name(message: types.Message, state: FSMContext):
    new_manager_name = message.text
    data = await state.get_data()
    service_id = data.get("service_id")

    if message.text == "◀️Orqaga":
        service = await db.get_service_by_id(service_id)
        if not service.success:
            return await message.answer(service.message)

        service = service.data

        managers = await db.get_service_managers(service_id)
        if not managers.success:
            return await message.answer(managers.message)

        managers = managers.data

        text = (
            "Menejerlar ro'yxati:\n"
            "Kerakli menejer tanlang yoki yangi menejer qo'shing."
        )
        await message.answer(
            text,
            reply_markup=select_manager_kb(managers, service_id),
        )
        await state.finish()
        return

    await state.update_data(new_manager_name=new_manager_name)

    await message.answer("Yangi menejer telefon raqamini kiriting:", reply_markup=back)
    await state.set_state("new_manager_phone")


@dp.message_handler(IsAdmin(), state="new_manager_phone")
async def new_manager_phone(message: types.Message, state: FSMContext):
    new_manager_phone = message.text

    if not validate_phone_number(new_manager_phone):
        await message.answer(
            "Noto'g'ri telefon raqam kiritildi. Iltimos, qaytadan kiriting.\n"
            "Masalan: +998901234567 yoki 998901234567",
            reply_markup=back,
        )
        return

    data = await state.get_data()
    service_id = data.get("service_id")
    new_manager_name = data.get("new_manager_name")

    if message.text == "◀️Orqaga":
        await message.answer("Yangi menejer ismini kiriting:", reply_markup=back)
        await state.set_state("new_manager_name")
        return

    db_response = await db.add_new_service_manager(
        service_id, new_manager_name, new_manager_phone
    )
    if not db_response.success:
        return await message.answer(db_response.message)

    managers = await db.get_service_managers(service_id)
    if not managers.success:
        return await message.answer(managers.message)
    managers = managers.data

    text = (
        "Menejerlar ro'yxati:\n" "Kerakli menejer tanlang yoki yangi menejer qo'shing."
    )
    await message.answer(
        text,
        reply_markup=select_manager_kb(managers, service_id),
    )
    await state.finish()
