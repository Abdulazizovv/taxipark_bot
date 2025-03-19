from aiogram import types
from bot.keyboards.inline.edit_driver_tarif import edit_driver_tariff_kb, edit_driver_tariff_cb
from bot.loader import dp, db
from bot.keyboards.inline import driver_detail_callback, edit_driver_detail_kb
from bot.keyboards.inline.edit_driver import edit_driver_info_kb, edit_driver_detail_cb
from aiogram.dispatcher import FSMContext


@dp.callback_query_handler(driver_detail_callback.filter(action="edit"))
async def edit_driver(call: types.CallbackQuery, callback_data: dict):
    driver_id = callback_data.get("driver_id")
    driver = await db.get_driver(driver_id=driver_id)
    if not driver.success:
        await call.message.answer(driver.message)
        return
    driver = driver.data
    await call.message.edit_text(
        f"Haydovchi haqidagi ma'lumotlar:\n\n"
        f"<b>👤 Ismi:</b> {driver['full_name']}\n"
        f"<b>📞 Telefon raqami:</b> {driver['phone_number']}\n"
        f"<b>🚗 Mashina modeli:</b> {driver['car_model']}\n"
        f"<b>🚖 Mashina raqami:</b> {driver['car_plate']}\n"
        f"<b>📦 Tarifi:</b> {driver['tariff']}\n"
        f"<b>💰 Balansi:</b> {driver['balance']} so'm",
        reply_markup=edit_driver_info_kb(driver_id),
    )


@dp.callback_query_handler(edit_driver_detail_cb.filter(action="back"))
async def back_to_driver_detail(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    driver_id = callback_data.get("driver_id")
    driver = await db.get_driver(driver_id=driver_id)
    if not driver.success:
        await call.message.answer(driver.message)
        return
    driver = driver.data
    await call.message.edit_text(
        f"Haydovchi haqidagi ma'lumotlar:\n\n"
        f"<b>👤 Ismi:</b> {driver['full_name']}\n"
        f"<b>📞 Telefon raqami:</b> {driver['phone_number']}\n"
        f"<b>🚗 Mashina modeli:</b> {driver['car_model']}\n"
        f"<b>🚖 Mashina raqami:</b> {driver['car_plate']}\n"
        f"<b>📦 Tarifi:</b> {driver['tariff']}\n"
        f"<b>💰 Balansi:</b> {driver['balance']} so'm",
        reply_markup=edit_driver_detail_kb(driver_id),
    )


@dp.callback_query_handler(driver_detail_callback.filter(action="delete"))
async def delete_driver(call: types.CallbackQuery, callback_data: dict):
    driver_id = callback_data.get("driver_id")
    if await db.delete_driver(driver_id=driver_id):
        await call.message.answer("Haydovchi o'chirildi!")
    else:
        await call.message.answer("Xatolik yuz berdi!")
    await call.message.delete()



@dp.callback_query_handler(edit_driver_detail_cb.filter(action="edit_full_name"))
async def edit_driver_full_name(
    call: types.CallbackQuery, callback_data: dict, state: FSMContext
):
    await call.message.edit_text("Ismni kiriting:")
    await state.update_data(driver_id=callback_data.get("driver_id"))
    await state.set_state("admin:edit_driver_full_name")


@dp.message_handler(state="admin:edit_driver_full_name")
async def get_driver_full_name(message: types.Message, state: FSMContext):
    full_name = message.text
    data = await state.get_data()
    driver_id = data.get("driver_id")
    if await db.edit_driver_full_name(driver_id=driver_id, full_name=full_name):
        driver = await db.get_driver(driver_id=driver_id)
        if not driver.success:
            await message.answer(driver.message)
            return
        driver = driver.data
        await message.answer(
            f"Haydovchi haqidagi ma'lumotlar:\n\n"
            f"<b>👤 Ismi:</b> {driver['full_name']}\n"
            f"<b>📞 Telefon raqami:</b> {driver['phone_number']}\n"
            f"<b>🚗 Mashina modeli:</b> {driver['car_model']}\n"
            f"<b>🚖 Mashina raqami:</b> {driver['car_plate']}\n"
            f"<b>📦 Tarifi:</b> {driver['tariff']}\n"
            f"<b>💰 Balansi:</b> {driver['balance']} so'm",
            reply_markup=edit_driver_info_kb(driver_id),
        )
    else:
        await message.answer("Xatolik yuz berdi!")
    await state.finish()


@dp.callback_query_handler(edit_driver_detail_cb.filter(action="edit_phone_number"))
async def edit_driver_phone_number(
    call: types.CallbackQuery, callback_data: dict, state: FSMContext
):
    await call.message.edit_text("Yangi telefon raqamni kiriting:")
    await state.update_data(driver_id=callback_data.get("driver_id"))
    await state.set_state("admin:edit_driver_phone_number")


@dp.message_handler(state="admin:edit_driver_phone_number")
async def get_driver_phone_number(message: types.Message, state: FSMContext):
    phone_number = message.text
    data = await state.get_data()
    driver_id = data.get("driver_id")
    if await db.edit_driver_phone_number(driver_id=driver_id, phone_number=phone_number):
        driver = await db.get_driver(driver_id=driver_id)
        if not driver.success:
            await message.answer(driver.message)
            return
        driver = driver.data
        await message.answer(
            f"Haydovchi haqidagi ma'lumotlar:\n\n"
            f"<b>👤 Ismi:</b> {driver['full_name']}\n"
            f"<b>📞 Telefon raqami:</b> {driver['phone_number']}\n"
            f"<b>🚗 Mashina modeli:</b> {driver['car_model']}\n"
            f"<b>🚖 Mashina raqami:</b> {driver['car_plate']}\n"
            f"<b>📦 Tarifi:</b> {driver['tariff']}\n"
            f"<b>💰 Balansi:</b> {driver['balance']} so'm",
            reply_markup=edit_driver_info_kb(driver_id),
        )
    else:
        await message.answer("Xatolik yuz berdi!")
    await state.finish()


@dp.callback_query_handler(edit_driver_detail_cb.filter(action="edit_car_model"))
async def edit_driver_car_model(
    call: types.CallbackQuery, callback_data: dict, state: FSMContext
):
    await call.message.edit_text("Mashina modelini kiriting:")
    await state.update_data(driver_id=callback_data.get("driver_id"))
    await state.set_state("admin:edit_driver_phone_number")


@dp.message_handler(state="admin:edit_driver_phone_number")
async def get_driver_car_model(message: types.Message, state: FSMContext):
    car_model = message.text
    data = await state.get_data()
    driver_id = data.get("driver_id")
    if await db.edit_driver_phone_number(driver_id=driver_id, car_model=car_model):
        driver = await db.get_driver(driver_id=driver_id)
        if not driver.success:
            await message.answer(driver.message)
            return
        driver = driver.data
        await message.answer(
            f"Haydovchi haqidagi ma'lumotlar:\n\n"
            f"<b>👤 Ismi:</b> {driver['full_name']}\n"
            f"<b>📞 Telefon raqami:</b> {driver['phone_number']}\n"
            f"<b>🚗 Mashina modeli:</b> {driver['car_model']}\n"
            f"<b>🚖 Mashina raqami:</b> {driver['car_plate']}\n"
            f"<b>📦 Tarifi:</b> {driver['tariff']}\n"
            f"<b>💰 Balansi:</b> {driver['balance']} so'm",
            reply_markup=edit_driver_info_kb(driver_id),
        )
    else:
        await message.answer("Xatolik yuz berdi!")
    await state.finish()


@dp.callback_query_handler(edit_driver_detail_cb.filter(action="edit_car_plate"))
async def edit_driver_car_plate(
    call: types.CallbackQuery, callback_data: dict, state: FSMContext
):
    await call.message.edit_text("Mashina raqamini kiriting:")
    await state.update_data(driver_id=callback_data.get("driver_id"))
    await state.set_state("admin:edit_driver_car_plate")


@dp.message_handler(state="admin:edit_driver_car_plate")
async def get_driver_car_model(message: types.Message, state: FSMContext):
    car_plate = message.text
    data = await state.get_data()
    driver_id = data.get("driver_id")
    if await db.edit_driver_car_plate(driver_id=driver_id, car_plate=car_plate):
        driver = await db.get_driver(driver_id=driver_id)
        if not driver.success:
            await message.answer(driver.message)
            return
        driver = driver.data
        await message.answer(
            f"Haydovchi haqidagi ma'lumotlar:\n\n"
            f"<b>👤 Ismi:</b> {driver['full_name']}\n"
            f"<b>📞 Telefon raqami:</b> {driver['phone_number']}\n"
            f"<b>🚗 Mashina modeli:</b> {driver['car_model']}\n"
            f"<b>🚖 Mashina raqami:</b> {driver['car_plate']}\n"
            f"<b>📦 Tarifi:</b> {driver['tariff']}\n"
            f"<b>💰 Balansi:</b> {driver['balance']} so'm",
            reply_markup=edit_driver_info_kb(driver_id),
        )
    else:
        await message.answer("Xatolik yuz berdi!")
    await state.finish()


@dp.callback_query_handler(edit_driver_detail_cb.filter(action="edit_tariff"))
async def edit_driver_tariff(
    call: types.CallbackQuery, callback_data: dict, state: FSMContext
):
    await call.message.edit_text("Tarifni tanlang:", reply_markup=edit_driver_tariff_kb(driver_id=callback_data.get("driver_id")))


@dp.callback_query_handler(edit_driver_detail_cb.filter(action="delete"))
async def delete_driver(call: types.CallbackQuery, callback_data: dict):
    driver_id = callback_data.get("driver_id")
    if await db.delete_driver(driver_id=driver_id):
        await call.message.answer("Haydovchi o'chirildi!")
    else:
        await call.message.answer("Xatolik yuz berdi!")
    await call.message.delete()
    

@dp.callback_query_handler(edit_driver_tariff_cb.filter())
async def edit_driver_tariff_action(call: types.CallbackQuery, callback_data: dict):
    driver_id = callback_data.get("driver_id")
    action = callback_data.get("action")
    if await db.edit_driver_tariff(driver_id=driver_id, tariff=action):
        driver = await db.get_driver(driver_id=driver_id)
        if not driver.success:
            await call.message.answer(driver.message)
            return
        driver = driver.data
        await call.message.edit_text(
            f"Haydovchi haqidagi ma'lumotlar:\n\n"
            f"<b>👤 Ismi:</b> {driver['full_name']}\n"
            f"<b>📞 Telefon raqami:</b> {driver['phone_number']}\n"
            f"<b>🚗 Mashina modeli:</b> {driver['car_model']}\n"
            f"<b>🚖 Mashina raqami:</b> {driver['car_plate']}\n"
            f"<b>📦 Tarifi:</b> {driver['tariff']}\n"
            f"<b>💰 Balansi:</b> {driver['balance']} so'm",
            reply_markup=edit_driver_info_kb(driver_id),
        )
    else:
        await call.message.edit("Xatolik yuz berdi!")


@dp.callback_query_handler(edit_driver_tariff_cb.filter(action="back"))
async def back_to_edit_driver(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    driver_id = callback_data.get("driver_id")
    driver = await db.get_driver(driver_id=driver_id)
    if not driver.success:
        await call.message.answer(driver.message)
        return
    driver = driver.data
    await call.message.edit_text(
        f"Haydovchi haqidagi ma'lumotlar:\n\n"
        f"<b>👤 Ismi:</b> {driver['full_name']}\n"
        f"<b>📞 Telefon raqami:</b> {driver['phone_number']}\n"
        f"<b>🚗 Mashina modeli:</b> {driver['car_model']}\n"
        f"<b>🚖 Mashina raqami:</b> {driver['car_plate']}\n"
        f"<b>📦 Tarifi:</b> {driver['tariff']}\n"
        f"<b>💰 Balansi:</b> {driver['balance']} so'm",
        reply_markup=edit_driver_info_kb(driver_id),
    )