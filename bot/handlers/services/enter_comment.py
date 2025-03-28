from aiogram import types
from bot.loader import dp, db
from aiogram.dispatcher import FSMContext
from bot.filters import IsService
from bot.keyboards.default import service_admin_menu_kb, back_kb, skip_kb
from bot.keyboards.inline.service.confirm_order import confirm_order_kb
from bot.utils.main import format_currency


@dp.message_handler(
    IsService(), state="enter_comment", content_types=types.ContentTypes.TEXT
)
async def enter_comment(message: types.Message, state: FSMContext):
    data = await state.get_data()
    driver_id = data.get("selected_driver")["id"]
    service = await db.get_service_by_id(data.get("service_id"))
    if not service.success:
        await message.answer(
            "Tanlangan xizmat bazada topilmadi!\n",
            reply_markup=service_admin_menu_kb,
        )
        await state.finish()
        return

    service = service.data

    comment = message.text

    if message.text == "O'tkazib yuborish ➡️":
        try:
            del_msg = await message.answer("...", reply_markup=types.ReplyKeyboardRemove())
            await dp.bot.delete_message(del_msg.chat.id, del_msg.message_id)
        except:
            pass
        comment = ""

    text = "".join(
        [
            f"<b>Xizmat:</b> {service['title']}\n\n",
            f"<b>Haydovchi:</b> {data.get('selected_driver')['car_model']} - {data.get('selected_driver')['car_plate']}\n\n",
            f"<b>Summa:</b> {format_currency(int(data.get('summa')))} so'm\n\n",
            f"<b>Izoh:</b> {comment}\n\n" if comment else "",
            f"Buyurtmani tasdiqlaysizmi?",
        ]
    )
    await state.update_data(comment=comment)
    await message.answer(
        text,
        reply_markup=confirm_order_kb(
            driver_id=driver_id,
            service_id=data.get("service_id"),
            summa=data.get("summa"),
        ),
    )
    await state.set_state("confirm_order")
