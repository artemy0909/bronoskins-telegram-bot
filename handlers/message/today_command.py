from aiogram import types
from aiogram.types import ReplyKeyboardRemove

from loader import dp, users, current_change
from ui.text import static
import ui.text.dynamic.today_command as dynamic
from utils.filters import AccessFilter
from utils.rights import ACCESS_FOR_ALL


@dp.message_handler(AccessFilter(*ACCESS_FOR_ALL), commands=['today'])
async def process_today_command(message: types.Message):
    user = users[message.from_user.id]
    user.del_all_dialog_data()
    if current_change.is_opened():
        await message.reply(
            reply_markup=ReplyKeyboardRemove(),
            text=dynamic.change_report(user, current_change.change))
    else:
        await message.reply(
            reply_markup=ReplyKeyboardRemove(),
            text=static.OPEN_CHANGE_REQUIRED)
