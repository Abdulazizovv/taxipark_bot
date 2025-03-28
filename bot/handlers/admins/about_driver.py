from aiogram import types
from bot.loader import dp, db
from bot.filters import IsAdmin
from aiogram.dispatcher.filters import Text
from bot.keyboards.inline import edit_driver_detail_kb
from bot.utils.main import format_currency


@dp.message_handler(IsAdmin(), Text(startswith="🚖"))
async def driver_details(message: types.Message):
    car_plate = message.text.split("🚖")[1].strip()
    driver = await db.get_driver_by_car_plate(car_plate)
    if driver:
        await message.answer(
            f"Haydovchi haqidagi ma'lumotlar:\n\n"
            f"<b>👤 Ismi:</b> {driver['full_name']}\n"
            f"<b>📞 Telefon raqami:</b> {driver['phone_number']}\n"
            f"<b>🚗 Mashina modeli:</b> {driver['car_model']}\n"
            f"<b>🚖 Mashina raqami:</b> {driver['car_plate']}\n"
            f"<b>📦 Tarifi:</b> {driver['tariff']}\n"
            f"<b>💰 Balansi:</b> {format_currency(int(driver['balance']))} so'm\n"
            f"<b>📅 Qo'shilgan vaqti</b>: {driver['created_at'].strftime('%d-%m-%Y %H:%M')}",
            reply_markup=edit_driver_detail_kb(driver["id"]),
        )
    else:
        await message.answer("Haydovchi topilmadi!")
