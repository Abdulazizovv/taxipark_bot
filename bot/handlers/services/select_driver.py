from aiogram import types
from bot.loader import dp, db
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from bot.keyboards.default import back_kb, service_admin_menu_kb
from bot.filters import IsService


@dp.message_handler(IsService(), Text(startswith="🚖"), state="select_driver")
async def select_driver(message: types.Message, state: FSMContext):
    driver = message.text
    driver_car_plate = driver.split("🚖")[1].strip()
    print(driver_car_plate)
        
    # tanlangan haydovchini bazadan olish
    driver = await db.get_driver_by_car_plate(car_plate=driver_car_plate)

    if driver is None:
        await message.answer("Haydovchi bazada topilmadi!", reply_markup=back_kb)
        return
    
    if driver['balance'] <= 0:
        await message.answer("Haydovchining balansida xizmat ko'rsatish uchun mablag' yetarli emas!", reply_markup=back_kb)
        return
    
    # tanlangan haydovchini state ga saqlash
    await state.update_data(selected_driver=driver)
    await message.answer(f"Haydovchi tanlandi: \n"
                         f"{driver['car_model']} - {driver['car_plate']}\n"
                         f"{driver['full_name']}\n\n"
                         f"Summani kiriting:", reply_markup=back_kb)
    await state.set_state("enter_sum")
    

@dp.message_handler(IsService(), text="◀️Orqaga", state="select_driver")
async def back_to_service(message: types.Message, state: FSMContext):
    await message.answer("Bosh menyuga qaytdingiz!", reply_markup=service_admin_menu_kb)
    await state.finish()
    return
