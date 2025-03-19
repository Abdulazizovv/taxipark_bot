from aiogram import types
from aiogram.dispatcher import FSMContext
from bot.loader import dp, db
from bot.keyboards.inline import driver_detail_callback
from bot.keyboards.inline import edit_driver_detail_kb


@dp.callback_query_handler(driver_detail_callback.filter(action="add_balance"))
async def add_balance(
    call: types.CallbackQuery, callback_data: dict, state: FSMContext
):
    driver_id = int(callback_data.get("driver_id"))
    await call.message.delete()
    await call.message.answer("Summani kiriting:")
    await state.set_state("add_balance")
    await state.update_data(driver_id=driver_id)


@dp.message_handler(state="add_balance")
async def add_balance(message: types.Message, state: FSMContext):
    data = await state.get_data()
    driver_id = data.get("driver_id")
    driver = await db.get_driver(driver_id)
    if not driver.success:
        await message.answer(driver.message)
        return
    driver = driver.data
    balance: str = message.text
    if balance.isdecimal() and int(balance) > 0:
        await db.add_balance(driver_id, int(balance))
        await message.answer(
            "Balans muvaffaqqiyatli o'zgartirildi!\n"
            f"<b>👤 Ismi:</b> {driver['full_name']}\n"
            f"<b>📞 Telefon raqami:</b> {driver['phone_number']}\n"
            f"<b>🚗 Mashina modeli:</b> {driver['car_model']}\n"
            f"<b>🚖 Mashina raqami:</b> {driver['car_plate']}\n"
            f"<b>📦 Tarifi:</b> {driver['tariff']}\n"
            f"<b>💰 Balansi:</b> {driver['balance']} so'm",
            reply_markup=edit_driver_detail_kb(driver_id),
        )
    else:
        await message.answer("Summa faqat raqamlardan tashkil topgan bo'lishi va 0 dan katta bo'lishi kerak!:")
        await state.set_state("add_balance")
        return
    await state.finish()
