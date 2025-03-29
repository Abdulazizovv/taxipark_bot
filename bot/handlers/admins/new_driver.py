from aiogram import types
from bot.loader import dp, db
from aiogram.dispatcher import FSMContext
from bot.keyboards.default import back_kb
from bot.keyboards.inline import submit_new_driver_kb
from bot.filters import IsAdmin
from bot.utils.main import validate_phone_number, validate_uzbek_car_plate


@dp.message_handler(IsAdmin(), text="Yangi haydovchi➕", state="*")
async def new_driver(message: types.Message, state: FSMContext):
    await state.finish()

    await message.answer("Haydovchi ism familyasini kiriting:", reply_markup=back_kb)
    await state.set_state("new_driver_name")


@dp.message_handler(IsAdmin(), state="new_driver_name")
async def new_driver_name(message: types.Message, state: FSMContext):
    driver_name = message.text

    await state.update_data(full_name=driver_name)

    await message.answer("Haydovchi telefon raqamini kiriting:\n\n"
                         "<i>misol uchun: +998YYXXXXXXX</i>", parse_mode="HTML", reply_markup=back_kb)
    await state.set_state("new_driver_number")


@dp.message_handler(IsAdmin(), state="new_driver_number")
async def new_driver_number(message: types.Message, state: FSMContext):
    driver_number = message.text
    if validate_phone_number(driver_number) is False:
        await message.answer("Telefon raqam noto'g'ri kiritildi!\n"
                             "<b>Telefon raqam formati:</b><i> +998XXYYYYYYY</i>", parse_mode="HTML", reply_markup=back_kb)
        return

    phone_number_exists = await db.check_phone_number_exists(phone_number=driver_number)
    if not phone_number_exists.success:
        await message.answer("Bu raqam avval ro'yxatdan o'tgan!", reply_markup=back_kb)
        return

    await state.update_data(phone_number=driver_number)

    await message.answer("Mashina modelini kiriting:", reply_markup=back_kb)
    await state.set_state("new_driver_car_model")


@dp.message_handler(IsAdmin(), state="new_driver_car_model")
async def new_driver_car_model(message: types.Message, state: FSMContext):
    car_model = message.text.upper()

    await state.update_data(car_model=car_model)

    await message.answer("Mashina raqamini kiriting:", reply_markup=back_kb)
    await state.set_state("new_driver_car_number")


@dp.message_handler(IsAdmin(), state="new_driver_car_number")
async def new_driver_car_number(message: types.Message, state: FSMContext):
    car_number = message.text.upper()
    if validate_uzbek_car_plate(car_number) is False:
        await message.answer("Mashina raqam noto'g'ri kiritildi!\n"
                             "<b>Mashina raqam formati:</b><i> 40A123AA yoki 40123AAA</i>", parse_mode="HTML", reply_markup=back_kb)
        return

    car_plate_exists = await db.check_car_plate(car_plate=car_number)
    if not car_plate_exists.success:
        await message.answer("Bu mashina raqami avval ro'yxatdan o'tgan!", reply_markup=back_kb)
        return

    await state.update_data(car_plate=car_number)

    await message.answer(
        "Haydovchi tarifini tanlang:",
        reply_markup=types.ReplyKeyboardMarkup(
            keyboard=[
                [
                    types.KeyboardButton(text="Standard"),
                    types.KeyboardButton(text="Comfort"),
                    types.KeyboardButton(text="Business"),
                    types.KeyboardButton(text="Premium"),
                ],
                [
                    types.KeyboardButton(text="◀️Orqaga"),
                ]
            ],
            resize_keyboard=True,
        ),
    )
    await state.set_state("new_driver_tariff")


@dp.message_handler(IsAdmin(), state="new_driver_tariff")
async def new_driver_tariff(message: types.Message, state: FSMContext):
    tariff = message.text

    if tariff not in ["Standard", "Comfort", "Business", "Premium"]:
        await message.answer(
            "Iltimos, quyidagi variantlardan birini tanlang!",
            reply_markup=types.ReplyKeyboardMarkup(
                keyboard=[
                    [
                        types.KeyboardButton(text="Standard"),
                        types.KeyboardButton(text="Comfort"),
                        types.KeyboardButton(text="Business"),
                        types.KeyboardButton(text="Premium"),
                    ]
                ],
                resize_keyboard=True,
            ),
        )
        await state.set_state("new_driver_tariff")
        return

    await state.update_data(tariff=tariff.lower())
    data = await state.get_data()

    await message.answer(
        "Ma'lumotlar qabul qilindi. Tasdiqlaysizmi?\n\n"
        f"<b>Ism:</b> {data.get('full_name')}\n"
        f"<b>Raqam:</b> {data.get('phone_number')}\n"
        f"<b>Model:</b> {data.get('car_model')}\n"
        f"<b>Raqam:</b> {data.get('car_plate')}\n"
        f"<b>Tarif:</b> {data.get('tariff')}",
        reply_markup=types.ReplyKeyboardRemove()  # ✅ Remove the keyboard here
    )

    await message.answer(
        "Davom etish uchun quyidagilardan birini tanlang:",
        reply_markup=submit_new_driver_kb()
    )
    await state.set_state("submit_new_driver")

    # data = await state.get_data()

    # driver_id = await db.add_new_driver(
    #     full_name=data.get("driver_name"),
    #     phone_number=data.get("driver_number"),
    #     car_model=data.get("car_model"),
    #     car_plate=data.get("car_number"),
    #     tariff=data.get("tariff"),
    # )

    # if driver_id is None:
    #     await message.answer("Haydovchi qo'shishda xatolik yuz berdi!")
    #     return

    # driver = await db.get_driver(driver_id=driver_id)

    # await message.answer(
    #     "Yangi haydovchi muvaffaqiyatli qo'shildi!\n"
    #     f"ID: <b>{driver['id']}</b>\n"
    #     f"Ism: <b>{driver['full_name']}</b>\n"
    #     f"Raqam: <b>{driver['phone_number']}</b>\n"
    #     f"Model: <b>{driver['car_model']}</b>\n"
    #     f"Raqam: <b>{driver['car_plate']}</b>\n"
    #     f"Tarif: <b>{driver['tariff']}</b>\n"
    #     f"Balans: <b>{driver['balance']}</b>\n",
    #     reply_markup=edit_driver_detail_kb(driver_id=driver_id),
    # )
