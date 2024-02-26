import os

from aiogram import types
from aiogram.types import InputFile

import states.reports_command as states

from loader import dp, users
import ui.keyboards.reply_keyboards.reports_command as reply_keyboards
from ui.text import static
from utils import file_generators
from utils.filters import AccessFilter, StateFilter
from utils.misc import MONTH_NAMINGS
from utils.rights import ACCESS_FOR_ADMINS

import config


@dp.message_handler(AccessFilter(*ACCESS_FOR_ADMINS), commands=['reports'])
async def process_reports_command(message: types.Message):
    user = users[message.from_user.id]
    user.del_all_dialog_data()
    user.state.set(states.REPORTS_MONTH_SELECTOR)
    await message.reply(
        reply_markup=reply_keyboards.get_month_year_keyboard(user),
        text=static.SELECT_MONTH)


@dp.message_handler(StateFilter(states.REPORTS_MONTH_SELECTOR), AccessFilter(*ACCESS_FOR_ADMINS))
async def reports_month_selector_line_callback(message: types.Message):
    user = users[message.from_user.id]
    if message.text in user["reports_links"]:
        await message.reply(
            text=static.PREPARING_FILE)
        month = user["reports_links"][message.text]
        file_path = file_generators.monthly_report_xlsx(month)
        await message.answer_document(
            InputFile(file_path, f"Отчет {config.MARKET_NAME} ({MONTH_NAMINGS[month[1]]} {month[0]}).xlsx"))
        os.remove(file_path)
        user.state.finish()
        user.del_all_dialog_data()
    else:
        await message.reply(
            text=static.INCORRECT_OPTION)
        await message.answer(
            reply_markup=reply_keyboards.get_month_year_keyboard(user),
            text=static.SELECT_MONTH)
