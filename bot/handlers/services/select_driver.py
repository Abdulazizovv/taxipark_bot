from aiogram import types
from bot.loader import dp, db
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text


@dp.message_handler(Text(startswith="🚖"), state="select_driver")
async def select_driver(message: types.Message, state: FSMContext):
    driver = message.text
    driver_car_plate = driver.split(" ")[1]
    
    # orqaga tugmasi bosilganda
    if driver == "⬅️ Orqaga":
        await message.answer("Haydovchini tanlang:", reply_markup=await db.get_drivers_keyboard())
        await state.set_state("select_driver")
        return
    
    # tanlangan haydovchini bazadan olish
    driver = await db.get_driver_by_car_plate(car_plate=driver_car_plate)

    if driver is None:
        await message.answer("Haydovchi bazada topilmadi!")
        return
    
    # tanlangan haydovchini state ga saqlash
    await state.update_data(selected_driver=driver)
    await message.answer(f"Haydovchi tanlandi: {driver['car_model']} - {driver['car_plate']}\n"
                         f"Summani kiriting:")
    await state.set_state("enter_sum")
    