from aiogram import types
from bot.loader import dp, db
from aiogram.dispatcher import FSMContext
from bot.filters import IsService
from bot.keyboards.default import service_admin_menu_kb, back_kb, skip_kb
from bot.keyboards.inline.service.confirm_order import confirm_order_kb


@dp.message_handler(
    IsService(), state="enter_sum", content_types=types.ContentTypes.TEXT
)
async def enter_summa(message: types.Message, state: FSMContext):
    if message.text == "◀️Orqaga":
        await state.finish()
        await message.answer(
            "Bosh menyuga qaytdingiz!", reply_markup=service_admin_menu_kb
        )
        return

    summa = message.text
    data = await state.get_data()
    driver_id = data.get("selected_driver")["id"]
    if summa.isdigit() and summa.isdigit() > 0:
        if not await db.enought_driver_balance(driver_id=driver_id, amount=int(summa)):
            await message.answer(
                "Haydovchi balansi yetarli emas!", reply_markup=back_kb
            )
            return
        await state.update_data(summa=summa)

        data = await state.get_data()
        service = await db.get_service_by_id(data.get("service_id"))
        if not service.success:
            await message.answer(
                "Tanlangan xizmat bazada topilmadi!\n",
                reply_markup=service_admin_menu_kb,
            )
            await state.finish()
            return

        service = service.data

        await message.answer("Buyurtma uchun izoh qoldiringiz mumkin...", reply_markup=skip_kb)
        await state.set_state("enter_comment")
        return

        
    else:
        await message.answer(
            "Summa noto'g'ri kiritildi! Qaytadan kiriting!", reply_markup=back_kb
        )
        return
