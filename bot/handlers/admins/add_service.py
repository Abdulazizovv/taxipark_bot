from asyncio import sleep
from aiogram import types
from aiogram.dispatcher import FSMContext

from bot.loader import dp, db
from bot.filters import IsAdmin
from bot.keyboards.inline.submit_service import submit_service_kb
from bot.keyboards.default import admin_menu_kb
from bot.keyboards.default.service_back import back_kb

# Constants for reusable messages
ENTER_SERVICE_NAME = (
    "Yangi servis nomini kiriting:\n"
    "<i>masalan: <b>Shaffof Gaz quyish shahobchasi</b></i>"
)

ENTER_DESCRIPTION = (
    "Servis haqida qisqacha ma'lumot bering:\n"
    "<i>masalan: <b>Chilonzor filiali</b></i>"
)

ENTER_PHONE = (
    "Servis uchun telefon raqamini kiriting:\n"
    "<i>masalan: <b>+998YYXXXXXXX</b></i>"
)

BACK_TO_MAIN_MENU = "Bosh menyuga qaytdingiz."


@dp.message_handler(IsAdmin(), text="Yangi servis➕", state="*")
async def add_service(message: types.Message, state: FSMContext) -> None:
    """Starts the process of adding a new service."""
    await state.finish()
    
    await message.answer(
        "Yangi servis qo'shish uchun kerakli ma'lumotlar:\n\n"
        "1️⃣ Servis nomi\n"
        "2️⃣ Servis haqida qisqacha ma'lumot\n"
        "3️⃣ Servis telefon raqami\n"
        "4️⃣ Servisni tasdiqlash\n"
    )

    await message.answer(ENTER_SERVICE_NAME, parse_mode="html", reply_markup=back_kb)
    await state.set_state("service_name")


@dp.message_handler(IsAdmin(), state="service_name")
async def get_service_name(message: types.Message, state: FSMContext) -> None:
    """Handles service name input."""
    if message.text.strip() == "⬅️Orqaga":
        await message.answer(BACK_TO_MAIN_MENU, reply_markup=admin_menu_kb)
        await state.finish()
        return

    service_name = message.text.strip()

    service_name_exists = await db.check_service_title_exists(service_name)
    if not service_name_exists.success:
        await message.answer(service_name_exists.message)
        return

    await state.update_data(service_name=service_name)
    await message.answer(ENTER_DESCRIPTION, parse_mode="html", reply_markup=back_kb)
    await state.set_state("service_description")


@dp.message_handler(IsAdmin(), state="service_description")
async def get_service_description(message: types.Message, state: FSMContext) -> None:
    """Handles service description input."""
    if message.text.strip() == "⬅️Orqaga":
        await message.answer(ENTER_SERVICE_NAME, parse_mode="html", reply_markup=back_kb)
        await state.set_state("service_name")
        return

    service_description = message.text.strip()
    await state.update_data(service_description=service_description)
    await message.answer(ENTER_PHONE, parse_mode="html", reply_markup=back_kb)
    await state.set_state("service_phone")


@dp.message_handler(IsAdmin(), state="service_phone")
async def get_service_phone(message: types.Message, state: FSMContext) -> None:
    """Handles service phone number input."""
    if message.text.strip() == "⬅️Orqaga":
        await message.answer(ENTER_DESCRIPTION, parse_mode="html", reply_markup=back_kb)
        await state.set_state("service_description")
        return

    service_phone = message.text.strip()
    await state.update_data(service_phone=service_phone)
    data = await state.get_data()

    await message.answer("⏳", reply_markup=types.ReplyKeyboardRemove())
    await sleep(1)
    
    await message.answer(
        "Ma'lumotlar qabul qilindi!\n"
        f"📌 <b>Servis nomi:</b> {data['service_name']}\n"
        f"📌 <b>Servis haqida:</b> {data['service_description']}\n"
        f"📌 <b>Telefon raqam:</b> {data['service_phone']}\n",
        parse_mode="html",
        reply_markup=submit_service_kb(),
    )


# @dp.message_handler(state="service_category")
# async def get_service_category(message: types.Message, state: FSMContext):

#     if message.text == "⬅️Orqaga":
#         await message.answer(
#             "Servis uchun telefon raqamini kiriting:\n"
#             "<i>masalan: <b>+998 99 999 99 99</b></i>",
#             parse_mode="html",
#             reply_markup=back_kb,
#         )
#         await state.set_state("service_phone")
#         return

#     data = await state.get_data()
#     service_category_name = message.text

#     service_category_names = data.get("service_category_names", [])

#     if message.text == "Davom etish▶️":

#         await message.answer("⏳", reply_markup=types.ReplyKeyboardRemove())
#         await sleep(1)
#         await message.answer(
#             "Ma'lumotlar qabul qilindi!\n"
#             f"Servis nomi: {data['service_name']}\n"
#             f"Servis haqida: {data['service_description']}\n"
#             f"Telefon raqam: {data['service_phone']}\n"
#             f"Kategoriyalar: {', '.join(service_category_names)}\n",
#             reply_markup=submit_service_kb(),
#         )
#         return

#     service_category_names.append(service_category_name)

#     service_category_response = await db.service_category_get_or_create(
#         service_category_name
#     )

#     if not service_category_response.success:
#         await message.answer(service_category_response.message)
#         return

#     service_category_id = service_category_response.data["category_id"]

#     await state.update_data(service_category_names=service_category_names)

#     service_category_ids = data.get("service_category_ids", [])
#     service_category_ids.append(service_category_id)
#     await state.update_data(service_category_ids=service_category_ids)

#     response = await db.exclude_service_categories(service_category_ids)

#     if not response.success:
#         await message.answer("⏳", reply_markup=types.ReplyKeyboardRemove())
#         await sleep(1)
#         await message.answer(
#             "Ma'lumotlar qabul qilindi!\n"
#             f"Servis nomi: {data['service_name']}\n"
#             f"Servis haqida: {data['service_description']}\n"
#             f"Telefon raqam: {data['service_phone']}\n"
#             f"Kategoriyalar: {', '.join(service_category_names)}\n",
#             reply_markup=submit_service_kb(),
#         )
#         return

#     service_categories = response.data

#     await message.answer(
#         "Kategoriya tanlandi!\n"
#         "Yana tanlashingiz mumkin. Agar tanlagan bo'lsa, tasdiqlash tugmasini bosing.",
#         reply_markup=service_category_add_kb(service_categories),
#     )
