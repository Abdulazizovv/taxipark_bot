from aiogram import types
from aiogram.dispatcher import FSMContext

from bot.loader import dp, db
from bot.filters import IsService
from bot.keyboards.default import service_admin_menu_kb
from bot.keyboards.inline.service.confirm_order import confirm_order_kb
from bot.utils.main import format_currency


async def safe_delete_message(message: types.Message) -> None:
    """Safely deletes a message to remove unnecessary UI clutter."""
    try:
        del_msg = await message.answer("...", reply_markup=types.ReplyKeyboardRemove())
        await dp.bot.delete_message(del_msg.chat.id, del_msg.message_id)
    except Exception as e:
        print(f"Error deleting message: {e}")  # Consider using logging instead of print


@dp.message_handler(IsService(), state="enter_comment", content_types=types.ContentTypes.TEXT)
async def enter_comment(message: types.Message, state: FSMContext) -> None:
    """Handles the user's comment input for an order."""
    
    data = await state.get_data()
    driver = data.get("selected_driver", {})
    service_response = await db.get_service_by_id(data.get("service_id"))

    if not service_response.success:
        await message.answer("Tanlangan xizmat bazada topilmadi!", reply_markup=service_admin_menu_kb)
        await state.finish()
        return

    service = service_response.data
    comment = message.text.strip()

    if comment == "O'tkazib yuborish ➡️":
        await safe_delete_message(message)
        comment = ""

    text = (
        f"<b>Xizmat:</b> {service['title']}\n\n"
        f"<b>Haydovchi:</b> {driver.get('car_model')} - {driver.get('car_plate')}\n\n"
        f"<b>Summa:</b> {format_currency(int(data.get('summa', 0)))} so'm\n\n"
        f"<b>Izoh:</b> {comment}\n\n" if comment else ""
        "Buyurtmani tasdiqlaysizmi?"
    )

    await state.update_data(comment=comment)
    await message.answer(
        text,
        reply_markup=confirm_order_kb(
            driver_id=driver.get("id"),
            service_id=data.get("service_id"),
            summa=data.get("summa"),
        ),
    )
    await state.set_state("confirm_order")
