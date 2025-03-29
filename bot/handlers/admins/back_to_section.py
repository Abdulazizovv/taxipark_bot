from aiogram import types
from aiogram.dispatcher import FSMContext
from bot.loader import dp
from bot.keyboards.default import back_kb, admin_menu_kb
from bot.filters import IsAdmin

# Define driver registration steps
DRIVER_STEPS = [
    "new_driver_name",
    "new_driver_number",
    "new_driver_car_model",
    "new_driver_car_number",
    "new_driver_tariff",
]

DRIVER_MESSAGES = {
    "new_driver_name": "Haydovchi ismini kiriting:",
    "new_driver_number": "Haydovchi telefon raqamini kiriting:",
    "new_driver_car_model": "Mashina modelini kiriting:",
    "new_driver_car_number": "Mashina raqamini kiriting:",
    "new_driver_tariff": "Haydovchi uchun tarifni tanlang:"
}

@dp.callback_query_handler(IsAdmin(), lambda call: call.data == "main_menu", state="*")
async def back_to_main_menu(call: types.CallbackQuery, state: FSMContext):
    """Handles returning to the main menu."""
    await call.message.edit_reply_markup()
    await call.message.answer("Bosh menyu", reply_markup=admin_menu_kb)
    await state.finish()

@dp.message_handler(IsAdmin(), text="◀️Orqaga", state="*")
async def back_to_section(message: types.Message, state: FSMContext):
    """Handles navigating back to the previous step in driver registration."""
    current_state = await state.get_state()

    # If at the first step, return to the main menu
    if current_state == DRIVER_STEPS[0]:
        await state.finish()
        await message.answer("Bosh menyu.", reply_markup=admin_menu_kb)
        return

    # Find the previous step
    if current_state in DRIVER_STEPS:
        current_index = DRIVER_STEPS.index(current_state)
        previous_state = DRIVER_STEPS[current_index - 1]
        previous_message = DRIVER_MESSAGES[previous_state]

        # Set the state to the previous step and send the appropriate message
        await state.set_state(previous_state)
        await message.answer(previous_message, reply_markup=back_kb)
        await state.update_data(section=previous_state, message=previous_message)
