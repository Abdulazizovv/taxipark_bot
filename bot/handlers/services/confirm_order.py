from aiogram import types
from bot.loader import dp, db
from aiogram.dispatcher import FSMContext
from bot.filters import IsService
from bot.keyboards.inline.service.confirm_order import confirm_order_cb
from bot.keyboards.default import service_admin_menu_kb


@dp.callback_query_handler(IsService(), confirm_order_cb.filter(), state="confirm_order")
async def confirm_order(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer(cache_time=60)
    try:
        await call.message.edit_reply_markup()
    except:
        pass
    if callback_data.get("action") == "confirm":
        driver_id = callback_data.get("driver_id")
        service_id = callback_data.get("service_id")
        summa = callback_data.get("summa")
        data = await state.get_data()
        comment = data.get("comment")
        order = await db.create_order(driver_id=driver_id, service_id=service_id, summa=summa, comment=comment)
        if not order.success:
            await call.message.answer(order.message)
            return
        await call.message.reply("Amaliyot muvaffaqqiyatli amalga oshirildi ✅\n"
                                 "Bosh menyuga qaytdingiz.", reply_markup=service_admin_menu_kb)
        await state.finish()
    else:
        await call.message.reply("Amaliyot bekor qilindi ❌\n"
                                 "Bosh menyuga qaytdingiz", reply_markup=service_admin_menu_kb)
        await state.finish()