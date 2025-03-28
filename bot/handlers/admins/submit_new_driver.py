from aiogram import types
from bot.loader import dp, db
from aiogram.dispatcher import FSMContext
from bot.keyboards.inline import submit_new_driver_cb
from bot.keyboards.inline import edit_driver_detail_kb
from asyncio import sleep
from bot.keyboards.default import admin_menu_kb


@dp.callback_query_handler(
    submit_new_driver_cb.filter(action="submit"), state="submit_new_driver"
)
async def submit_new_driver(
    call: types.CallbackQuery, callback_data: dict, state: FSMContext
):
    data = await state.get_data()

    new_driver = await db.add_new_driver(
        full_name=data["full_name"],
        phone_number=data["phone_number"],
        car_model=data["car_model"],
        car_plate=data["car_plate"],
        tariff=data["tariff"],
    )

    if not new_driver.success:
        await call.message.answer(new_driver.message)
        return

    driver = await db.get_driver(driver_id=new_driver.data["driver_id"])
    if not driver.success:
        await call.message.answer(driver.message)
        return

    driver = driver.data

    try:
        await call.message.delete()
    except:
        await call.message.edit_reply_markup()

    await call.message.answer("⏳", reply_markup=types.ReplyKeyboardRemove())
    await sleep(1)

    text = "\n".join(
        [
            "Yangi haydovchi muvaffaqiyatli qo'shildi✅\n",
            f"Haydovchi: {driver['full_name']}",
            f"Telefon raqami: {driver['phone_number']}",
            f"Mashina modeli: {driver['car_model']}",
            f"Mashina raqami: {driver['car_plate']}",
            f"Tarif: {driver['tariff']}",
            f"Balans: {driver['balance']}",
        ]
    )

    await call.message.answer(
        text,
        reply_markup=edit_driver_detail_kb(driver_id=driver["id"]),
        parse_mode="HTML",
    )

    await state.finish()


@dp.callback_query_handler(submit_new_driver_cb.filter(action="cancel"), state="*")
async def cancel_submit_new_driver(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.delete()
    await call.message.answer("Haydovchi qo'shish bekor qilindi❌", reply_markup=admin_menu_kb)
    await state.finish()
    return
