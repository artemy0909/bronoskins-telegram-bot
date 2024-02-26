import re

from aiogram import types
from aiogram.types import ReplyKeyboardRemove

import states.cash_command as states
import ui.text.dynamic.cash_command as dynamic
from loader import dp, users
from ui.keyboards import buttons_text
from ui.keyboards.reply_keyboards.misc import CONFIRM_KEYBOARD
from ui.text import static
from utils.database import CashWithdrawal
from utils.filters import AccessFilter, StateFilter
from utils.rights import ACCESS_FOR_ALL


@dp.message_handler(AccessFilter(*ACCESS_FOR_ALL), commands=['cash'])
async def cash_command(message: types.Message):
    user = users[message.from_user.id]
    user.del_all_dialog_data()
    user.state.jump(states.cash_group)
    await message.reply(
        reply_markup=ReplyKeyboardRemove(),
        text=dynamic.write_num_to_withdrawal(user))


@dp.message_handler(StateFilter(states.CASH_COUNT), AccessFilter(*ACCESS_FOR_ALL))
async def money_count_callback(message: types.Message):
    user = users[message.from_user.id]
    if re.match(r"^-?\d+$", message.text):
        user["money_count"] = int(message.text)
        user.state.next()
        await message.reply(
            text=dynamic.confirm_withdrawal(user),
            reply_markup=CONFIRM_KEYBOARD)
    else:
        await message.reply(
            text=static.INCORRECT_SYMBOLS_USED)
        await message.answer(
            text=dynamic.write_num_to_withdrawal(user))


@dp.message_handler(StateFilter(states.CASH_PAYOFF_CONFIRM), AccessFilter(*ACCESS_FOR_ALL))
async def money_withdraw_confirm_callback(message: types.Message):
    user = users[message.from_user.id]
    if message.text == buttons_text.OK:
        cash_withdrawal = CashWithdrawal.create(money=user["money_count"], worker=user.im)
        user.state.finish()
        user.del_all_dialog_data()
        await message.reply(
            text=cash_withdrawal.full_view(is_admin=user.is_admin()))
    elif message.text == buttons_text.CANCEL:
        user.state.prev()
        await message.reply(
            text=dynamic.write_num_to_withdrawal(user))
    else:
        await message.reply(
            text=static.INCORRECT_OPTION)
        await message.answer(
            reply_markup=CONFIRM_KEYBOARD,
            text=dynamic.confirm_withdrawal(user))
