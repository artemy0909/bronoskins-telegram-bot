import re

from aiogram import types

import states.cuts_command as states
import ui.keyboards.inline_keyboards.cuts_actions as inline_keyboards
from ui.keyboards.reply_keyboards.misc import CONFIRM_KEYBOARD
from ui.keyboards import buttons_text
from ui.text import static
import ui.text.dynamic.cuts_command as dynamic

from loader import dp, users
from utils.database import ResIncoming
from utils.filters import StateFilter, AccessFilter
from utils.rights import ACCESS_FOR_ADMINS


@dp.message_handler(AccessFilter(*ACCESS_FOR_ADMINS), commands=['cuts'])
async def process_cuts_command(message: types.Message):
    user = users[message.from_user.id]
    user.del_all_dialog_data()
    user.state.jump(states.cuts_add_group)
    await message.reply(
        text=dynamic.type_res_count())


@dp.message_handler(StateFilter(states.CUTS_COUNT), AccessFilter(*ACCESS_FOR_ADMINS))
async def res_count_callback(message: types.Message):
    user = users[message.from_user.id]
    if re.match(r"^-?\d+$", message.text):
        user["res_count"] = int(message.text)
        user.state.next()
        await message.reply(
            text=static.TYPE_CUT_PRICE)
    else:
        await message.reply(
            text=static.INCORRECT_OPTION)
        await message.answer(
            text=dynamic.type_res_count())


@dp.message_handler(StateFilter(states.CUTS_PRICE), AccessFilter(*ACCESS_FOR_ADMINS))
async def cuts_price_callback(message: types.Message):
    user = users[message.from_user.id]
    if re.match(r"^\d+$", message.text):
        user["cuts_price"] = int(message.text)
        user.state.next()
        await message.reply(
            text=dynamic.cuts_add_confirm(user),
            reply_markup=CONFIRM_KEYBOARD)
    else:
        await message.reply(
            text=static.INCORRECT_OPTION)
        await message.answer(
            text=static.TYPE_CUT_PRICE)


@dp.message_handler(StateFilter(states.CUTS_ADD_CONFIRM), AccessFilter(*ACCESS_FOR_ADMINS))
async def cuts_add_confirm_callback(message: types.Message):
    user = users[message.from_user.id]
    if message.text == buttons_text.OK:
        res_incoming = ResIncoming.create(count=user["res_count"], unit_cost=user["cuts_price"])
        user.state.finish()
        user.del_all_dialog_data()
        await message.reply(
            reply_markup=inline_keyboards.res_incoming_actions(user, res_incoming),
            text=res_incoming.full_view(is_admin=True))
    elif message.text == buttons_text.CANCEL:
        user.state.prev()
        await message.reply(
            text=static.TYPE_CUT_PRICE)
    else:
        await message.reply(
            text=static.INCORRECT_OPTION)
        await message.answer(
            text=dynamic.cuts_add_confirm(user),
            reply_markup=CONFIRM_KEYBOARD)
