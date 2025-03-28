from aiogram import types
from aiogram.dispatcher import FSMContext
from bot.loader import dp, db
from bot.keyboards.inline import driver_detail_callback
from bot.keyboards.inline import edit_driver_detail_kb
from bot.keyboards.default import back_kb
from bot.utils.main import format_currency


@dp.callback_query_handler(driver_detail_callback.filter(action="add_balance"))
async def add_balance(
    call: types.CallbackQuery, callback_data: dict, state: FSMContext
):
    driver_id = int(callback_data.get("driver_id"))
    await call.message.edit_reply_markup()
    await call.message.answer("Summani kiriting:", reply_markup=back_kb)
    await state.set_state("add_balance")
    await state.update_data(driver_id=driver_id)


@dp.message_handler(state="add_balance")
async def add_balance(message: types.Message, state: FSMContext):
    data = await state.get_data()

    driver_id = data.get("driver_id")

    driver = await db.get_driver(driver_id)

    if not driver.success:
        await message.answer(driver.message)
        return
    driver = driver.data

    try:
        del_msg = await message.answer("...", reply_markup=types.ReplyKeyboardRemove())
        await dp.bot.delete_message(
            chat_id=del_msg.chat.id, message_id=del_msg.message_id
        )
    except:
        pass

    if message.text == "◀️Orqaga":
        await message.answer(
            f"Haydovchi ma'lumotlari!\n"
            f"<b>👤 Ismi:</b> {driver['full_name']}\n"
            f"<b>📞 Telefon raqami:</b> {driver['phone_number']}\n"
            f"<b>🚗 Mashina modeli:</b> {driver['car_model']}\n"
            f"<b>🚖 Mashina raqami:</b> {driver['car_plate']}\n"
            f"<b>📦 Tarifi:</b> {driver['tariff']}\n"
            f"<b>💰 Balansi:</b> {format_currency(int(driver['balance']))} so'm",
            reply_markup=edit_driver_detail_kb(driver_id),
        )
        await state.finish()
        return

    balance: str = message.text

    if balance.lstrip("-").isdigit():
        balance = int(balance)        

        if balance == 0:
            await message.answer(
                "<i>Summa 0 bo'lishi mumkin emas!</i>", parse_mode="HTML"
            )
            return
        
        if balance < 0:
            await message.answer("Siz hisobdan mablag' ayirmoqdasiz!\n"
                                 "Buning uchun izoh yozing!", reply_markup=back_kb)
            await state.update_data(balance=balance)
            await state.set_state("add_balance_comment")
            return

        # balans to'ldirishni tasdiqlash
        await message.answer(
            f"Balansni {format_currency(int(balance))} so'm ga o'zgartirishni tasdiqlaysizmi?",
            reply_markup=types.InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        types.InlineKeyboardButton(
                            text="Ha✅",
                            callback_data=f"confirm_balance:{balance}:{driver_id}",
                        ),
                        types.InlineKeyboardButton(
                            text="Yo'q❌", callback_data=f"cancel_balance:{driver_id}"
                        ),
                    ]
                ]
            ),
        )

    else:
        await message.answer(
            "<i>Summa faqat raqamlardan tashkil topgan bo'lishi va 0 dan katta bo'lishi kerak!</i>",
            parse_mode="HTML",
            reply_markup=back_kb,
        )
        await state.set_state("add_balance")
        return
    await state.finish()


@dp.callback_query_handler(
    lambda call: call.data.startswith("cancel_balance"), state="*"
)
async def cancel_balance(call: types.CallbackQuery, state: FSMContext):
    driver_id = int(call.data.split(":")[-1])
    driver = await db.get_driver(driver_id)
    if not driver.success:
        await call.message.answer(driver.message)
        return
    driver = driver.data
    await call.message.answer(
        f"Balansni o'zgartirish bekor qilindi!\n\n"
        f"Haydovchi ma'lumotlari!\n"
        f"<b>👤 Ismi:</b> {driver['full_name']}\n"
        f"<b>📞 Telefon raqami:</b> {driver['phone_number']}\n"
        f"<b>🚗 Mashina modeli:</b> {driver['car_model']}\n"
        f"<b>🚖 Mashina raqami:</b> {driver['car_plate']}\n"
        f"<b>📦 Tarifi:</b> {driver['tariff']}\n"
        f"<b>💰 Balansi:</b> {format_currency(int(driver['balance']))} so'm",
        parse_mode="HTML",
        reply_markup=edit_driver_detail_kb(driver_id),
    )

    await state.finish()


@dp.callback_query_handler(
    lambda call: call.data.startswith("confirm_balance"), state="*"
)
async def confirm_balance(call: types.CallbackQuery, state: FSMContext):
    balance = int(call.data.split(":")[1])
    driver_id = int(call.data.split(":")[-1])
    data = await state.get_data()
    comment = data.get("comment")

    driver = await db.add_balance(driver_id, balance, comment)
    if not driver:
        await call.message.answer("Nimadir xato bo'ldi!")
        return
    
    driver = await db.get_driver(driver_id)
    if not driver.success:
        await call.message.answer(driver.message)
        return
    driver = driver.data

    await call.message.delete()
    await call.message.answer(
        f"Balansni {format_currency(balance)} so'm ga o'zgartirish muvaffaqiyatli amalga oshirildi!\n\n"
        f"Haydovchi ma'lumotlari!\n"
        f"<b>👤 Ismi:</b> {driver['full_name']}\n"
        f"<b>📞 Telefon raqami:</b> {driver['phone_number']}\n"
        f"<b>🚗 Mashina modeli:</b> {driver['car_model']}\n"
        f"<b>🚖 Mashina raqami:</b> {driver['car_plate']}\n"
        f"<b>📦 Tarifi:</b> {driver['tariff']}\n"
        f"<b>💰 Balansi:</b> {format_currency(int(driver['balance']))} so'm",
        parse_mode="HTML",
        reply_markup=edit_driver_detail_kb(driver_id),
    )

    await state.finish()


@dp.message_handler(state="add_balance_comment")
async def add_balance_comment(message: types.Message, state: FSMContext):
    data = await state.get_data()

    driver_id = data.get("driver_id")

    driver = await db.get_driver(driver_id)

    if not driver.success:
        await message.answer(driver.message)
        return
    driver = driver.data

    if message.text == "◀️Orqaga":
        await message.answer("Summani kiriting:", reply_markup=back_kb)
        await state.set_state("add_balance")
        return

    comment = message.text
    await state.update_data(comment=comment)
    balance = data.get("balance")

    # balans to'ldirishni tasdiqlash
    await message.answer(
        f"Balansni {format_currency(int(balance))} so'm ga o'zgartirishni tasdiqlaysizmi?",
        reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    types.InlineKeyboardButton(
                        text="Ha✅",
                        callback_data=f"confirm_balance:{balance}:{driver_id}",
                    ),
                    types.InlineKeyboardButton(
                        text="Yo'q❌", callback_data=f"cancel_balance:{driver_id}"
                    ),
                ]
            ]
        ),
    )



