from aiogram import types
from bot.loader import dp, db
from bot.filters import IsAdmin
from aiogram.dispatcher import FSMContext


@dp.message_handler(IsAdmin(), text="📊Statistika", state="*")
async def show_statistics(message: types.Message, state: FSMContext):
    await state.finish()

    user_statistics = await db.get_users_stats()
    driver_statistics = await db.get_drivers_stats()
    service_statistics = await db.get_services_stats()
    transaction_statistics = await db.get_transactions_stats()

    text = f"<b>👤 Foydalanuvchilar:</b>\n" \
    f"Jami(botga start bosgan): {user_statistics['all_users']}\n"\
    f"Aktiv: {user_statistics['connected_users']}\n"\
    f"Adminlar: {user_statistics['manager_users']}\n"\
    f"Managerlar: {user_statistics['service_users']}\n\n"\
    f"<b>🚖 Haydovchilar:</b>\n" \
    f"Jami: {driver_statistics['count']}\n"\
    f"Faol: {driver_statistics['active_drivers']}\n\n"\
    f"<b>🔧 Xizmatlar:</b>\n" \
    f"Jami: {service_statistics['count']}\n\n"\
    f"<b>💰Tranzaksiyalar:</b>\n" \
    f"Jami: {transaction_statistics['count']}\n"

    await message.answer(text)