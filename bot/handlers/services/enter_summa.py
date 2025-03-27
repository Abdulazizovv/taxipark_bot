from aiogram import types
from bot.loader import dp, db
from aiogram.dispatcher import FSMContext
from bot.filters import IsService


@dp.message_handler(IsService(), state="enter_sum", content_types=types.ContentTypes.TEXT)
async def enter_summa(message: types.Message, state: FSMContext):
    summa = message.text
    data = await state.get_data()
    driver_id = data.get("selected_driver")["id"]
    if summa.isdigit() and summa.isdigit() > 0:
        print(summa)
        if not await db.enought_driver_balance(driver_id=driver_id, amount=int(summa)):
            await message.answer("Haydovchi balansi yetarli emas!")
            return
        await state.update_data(summa=summa)
        await message.answer("Summa qabul qilindi! 🤑")
        await state.set_state("confirm_order")
    else:
        await message.answer("Summa noto'g'ri kiritildi! Qaytadan kiriting!")
        return
