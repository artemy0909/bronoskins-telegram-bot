from datetime import datetime

from aiogram import types
from aiogram.types import InputFile
from aiogram.utils.markdown import hbold

import states.change_command as states
import ui.keyboards.inline_keyboards.bronoskin_actions as inline_keyboards
from ui.text import static
import ui.text.dynamic.change_command as dynamic

import config
from loader import dp, users, bot, current_change
from utils.filters import StateFilter, AccessFilter
from utils.misc import FATHER_ID, BASE_DATETIME_FORMAT
from utils.rights import ACCESS_FOR_ALL, admins_ids


@dp.message_handler(AccessFilter(*ACCESS_FOR_ALL), commands=['change'])
async def process_open_command(message: types.Message):
    user = users[message.from_user.id]
    user.del_all_dialog_data()
    if not current_change.is_opened():
        user.state.set(states.OPEN_CHANGE)
        await message.reply(
            text=static.OPEN_CHANGE)
    else:
        user.state.set(states.CLOSE_CHANGE)
        await message.reply(
            text=static.CLOSE_CHANGE)


@dp.message_handler(
    AccessFilter(*ACCESS_FOR_ALL),
    StateFilter(states.OPEN_CHANGE),
    content_types=['photo'])
async def open_change_callback(message: types.Message):
    user = users[message.from_user.id]
    if message.media_group_id:
        await message.reply(text=static.ONLY_ONE_PHOTO)
    else:
        photo_id = message.photo[-1].file_id
        current_change.open_change(user.im)
        text = dynamic.change_opened(current_change.change)
        for user_id in admins_ids():
            if user_id != message.from_user.id:
                await bot.send_photo(user_id, photo_id, text)
        user.del_all_dialog_data()
        user.state.finish()
        await message.reply(text)


@dp.message_handler(
    AccessFilter(*ACCESS_FOR_ALL),
    StateFilter(states.CLOSE_CHANGE),
    content_types=['photo'])
async def close_change_callback(message: types.Message):
    user = users[message.from_user.id]
    if message.media_group_id:
        await message.reply(text=static.ONLY_ONE_PHOTO)
    else:
        photo_id = message.photo[-1].file_id
        text = dynamic.change_closed_for_admins(current_change.change)
        for user_id in admins_ids():
            await bot.send_photo(user_id, photo_id, text)
            await bot.send_message(
                user_id, hbold("ДЕТАЛИЗАЦИЯ РЕЗОВ"),
                reply_markup=inline_keyboards.change_view_skins(users[user_id], current_change.change))
        user.del_all_dialog_data()
        user.state.finish()
        await bot.send_document(
            FATHER_ID, InputFile(config.DB_FILE),
            caption=f"Резервная копия базы данных от {datetime.now().strftime(BASE_DATETIME_FORMAT)}")
        await message.reply(text=dynamic.change_closed_for_worker(user, current_change.change))
        current_change.close_change()
