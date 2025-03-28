from aiogram import types
from bot.keyboards.default import service_admin_menu_kb
from bot.keyboards.default.service.select_service import select_service_keyboard
from bot.loader import dp, db
from bot.filters import IsService
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher import FSMContext
from bot.keyboards.inline.service.report_paginator import get_pagination_keyboard
import pandas as pd
import io
from bot.utils.main import format_currency
from datetime import datetime


@dp.message_handler(IsService(), Command("statistics"))
@dp.message_handler(IsService(), text="📊 Hisobotlar")
async def show_statistics(message: types.Message, state: FSMContext):
    if message.text == "🔙 Orqaga":
        await state.finish()
        return await message.answer("Bosh menyu", reply_markup=service_admin_menu_kb)
    
    services = await db.get_user_services(message.from_user.id)
    if not services.success:
        return await message.answer(services.message)
    services = services.data

    if not services:
        await message.answer("Sizda xizmatlar mavjud emas")
        return
    
    if len(services) == 1:
        await state.update_data(service_id=services[0]["id"])
        response = await db.get_service_transactions(services[0]["id"])
        if not response.success:
            return await message.answer(response.message)
        transactions = response.data
        if not transactions:
            return await message.answer("Hisobotlar mavjud emas")
        
        try:
            del_msg = await message.answer("1 soniya ...", reply_markup=types.ReplyKeyboardRemove())
            await dp.bot.delete_message(del_msg.chat.id, del_msg.message_id)
        except:
            pass
        
        transactions = response.data.get("transactions", [])
        current_page = response.data["current_page"]
        total_pages = response.data["total_pages"]
        message_text = "📊 Tranzaksiyalar:\n\n"
        for trx in transactions:
            message_text += (
                f"📍 ID: {trx['id']}\n"
                f"👤 Haydovchi: {trx['driver']['full_name']}\n"
                f"🚖 Mashina: {trx['driver']['car_model']} | {trx['driver']['car_plate']}\n"
                f"💰 Miqdor: {format_currency(abs(int(trx['amount'])))} so'm\n"
                f"📅 Vaqt: {trx['created_at'].strftime('%d-%m-%Y %H:%M')}\n"
                f"📝 Izoh: {trx['description'] or 'Yo‘q'}\n\n"
            )

        await message.answer(
            message_text,
            reply_markup=get_pagination_keyboard(services[0]["id"], current_page, total_pages)
        )    

        return
    
    await message.answer(
        "Hisobotlar uchun xizmat tanlang",
        reply_markup=select_service_keyboard(services),
    )
    await state.set_state("transactions:select_service")
    

@dp.message_handler(IsService(), state="transactions:select_service")
async def select_service(message: types.Message, state: FSMContext):
    if message.text == "🔙 Orqaga":
        await state.finish()
        return await message.answer("Bosh menyu", reply_markup=service_admin_menu_kb)
    
    service = await db.get_service_by_title(message.text)
    if not service.success:
        return await message.answer(service.message)
    
    service = service.data
    if not service:
        return await message.answer("Xizmat topilmadi")
    
    await state.update_data(service_id=service["id"])
    response = await db.get_service_transactions(service["id"], page=1, per_page=5)

    if not response.success:
        return await message.answer(response.message)
    
    transactions = response.data.get("transactions", [])
    current_page = response.data["current_page"]
    total_pages = response.data["total_pages"]

    if not transactions:
        return await message.answer("Hisobotlar mavjud emas")
    try:
        del_msg = await message.answer("1 soniya ...", reply_markup=types.ReplyKeyboardRemove())
        await dp.bot.delete_message(del_msg.chat.id, del_msg.message_id)
    except:
        pass

    message_text = "📊 Tranzaksiyalar:\n\n"
    for trx in transactions:
        message_text += (
            f"📍 ID: {trx['id']}\n"
            f"👤 Haydovchi: {trx['driver']['full_name']}\n"
            f"🚖 Mashina: {trx['driver']['car_model']} | {trx['driver']['car_plate']}\n"
            f"💰 Miqdor: {format_currency(abs(int(trx['amount'])))} so'm\n"
            f"📅 Vaqt: {trx['created_at'].strftime('%d-%m-%Y %H:%M')}\n"
            f"📝 Izoh: {trx['description'] or 'Yo‘q'}\n\n"
        )

    await message.answer(
        message_text,
        reply_markup=get_pagination_keyboard(service["id"], current_page, total_pages)
    )


@dp.callback_query_handler(lambda c: c.data == "back:transactions", state="*")
async def back_to_services(callback: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await callback.message.edit_reply_markup()
    services = await db.get_user_services(callback.from_user.id)
    if not services.success:
        await callback.answer()
        return await callback.message.answer(services.message)
    services = services.data

    if len(services) == 1:
        await callback.answer()
        await state.finish()
        await callback.message.answer("Bosh menyuga qaytdingiz!", reply_markup=service_admin_menu_kb)

        return

    await callback.message.answer("Hisobotlarni ko'rish uchun servisni tanlang", reply_markup=select_service_keyboard(services))
    await state.set_state("transactions:select_service")
    await callback.answer()


@dp.callback_query_handler(lambda c: c.data.startswith("transactions:"), state="*")
async def paginate_transactions(callback: types.CallbackQuery):
    
    _, service_id, page = callback.data.split(":")
    service_id, page = int(service_id), int(page)

    response = await db.get_service_transactions(service_id, page=page, per_page=5)

    if not response.success:
        return await callback.answer(response.message, show_alert=True)

    transactions = response.data.get("transactions", [])
    current_page = response.data["current_page"]
    total_pages = response.data["total_pages"]

    if not transactions:
        return await callback.answer("Hisobotlar mavjud emas", show_alert=True)

    message_text = "📊 Tranzaksiyalar:\n\n"
    for trx in transactions:
        message_text += (
            f"📍 ID: {trx['id']}\n"
            f"👤 Haydovchi: {trx['driver']['full_name']}\n"
            f"🚖 Mashina: {trx['driver']['car_model']} | {trx['driver']['car_plate']}\n"
            f"💰 Miqdor: {format_currency(abs(int(trx['amount'])))} so'm\n"
            f"📅 Vaqt: {trx['created_at'].strftime('%d-%m-%Y %H:%M')}\n"
            f"📝 Izoh: {trx['description'] or 'Yo‘q'}\n"
            "--------------------------------\n"
        )

    await callback.message.edit_text(
        message_text,
        reply_markup=get_pagination_keyboard(service_id, current_page, total_pages)
    )
    await callback.answer()


@dp.callback_query_handler(lambda c: c.data == "ignore", state="*")
async def ignore(callback: types.CallbackQuery):
    await callback.answer()



@dp.callback_query_handler(lambda c: c.data.startswith("download:transactions"), state="*")
async def download_transactions_excel(callback: types.CallbackQuery, state: FSMContext):
    service_id = str(callback.data).split(":")[-1]
    await callback.answer("Yuklanmoqda...")
    if not service_id:
        return await callback.answer("Xizmat ID kiritilmadi", show_alert=True) 

    response = await db.get_service_all_transactions(service_id)
    if not response.success:
        return await callback.answer(response.message, show_alert=True)

    transactions = response.data or []
    if not transactions:
        return await callback.answer("Hisobotlar mavjud emas", show_alert=True)
    

    data = [
        {
            "ID": trx["id"],
            "Haydovchi": trx["driver"]["full_name"],
            "Mashina": f"{trx['driver']['car_model']} - {trx['driver']['car_plate']}",
            "Summa": str(format_currency(abs(int(trx["amount"])))) + " so'm",
            "Tavsif": trx["description"],
            "Vaqt": trx["created_at"].strftime("%d-%m-%Y %H:%M"),
        }
        for trx in transactions
    ]

    df = pd.DataFrame(data)
    
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Transactions")

    output.seek(0)

    now = datetime.now().strftime("%d-%m-%Y %H-%M")

    try:
        await callback.message.answer_document(
            types.InputFile(output, filename=f"hisobot {now}.xlsx"),
            caption="📊 Hisobotlar"
        )
        await callback.answer()
    except Exception as e:
        await callback.answer(f"Fayl yuborishda xatolik bo'ldi", show_alert=True)