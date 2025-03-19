from aiogram import types
from aiogram.dispatcher import FSMContext
from bot.loader import dp
from bot.keyboards.default import back_kb, admin_menu_kb


@dp.message_handler(text="◀️Orqaga", state="*")
async def back_to_section(message: types.Message, state: FSMContext):
    data = await state.get_data()

    # Get current state
    current_state = await state.get_state()

    # Get the steps and messages
    steps = [
        "new_driver_name",
        "new_driver_number",
        "new_driver_car_model",
        "new_driver_car_number",
        "new_driver_tariff",
    ]
    messages = {
        "new_driver_name": "Haydovchi ismini kiriting:",
        "new_driver_number": "Haydovchi telefon raqamini kiriting:",
        "new_driver_car_model": "Mashina modelini kiriting:",
        "new_driver_car_number": "Mashina raqamini kiriting:",
        "new_driver_tariff": "Haydovchi uchun tarifni tanlang:"
    }

    if current_state == "new_driver_name":
        await state.finish()
        await message.answer("Bosh menyu", reply_markup=admin_menu_kb)
        return

    # Find the index of the current step
    if current_state in steps:
        current_index = steps.index(current_state)
        previous_state = steps[current_index - 1]  # Get the previous step
        previous_message = messages[previous_state]  # Get the message

        # Set the previous state
        await state.set_state(previous_state)
        await message.answer(previous_message, reply_markup=back_kb)
        await state.update_data(section=previous_state, message=previous_message)