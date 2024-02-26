from datetime import datetime

from aiogram.types import CallbackQuery

import states.bronoskin_actions as states
import ui.keyboards.reply_keyboards.bronoskin_actions as reply_keyboards
import ui.keyboards.inline_keyboards.bronoskin_actions as inline_keyboards
from ui.keyboards.reply_keyboards.misc import CONFIRM_KEYBOARD
import ui.text.dynamic.bronoskin_actions as dynamic
from ui.text import static

from loader import dp, users, current_change
from ui import inline_commands
from utils.database import BronoSkin
from utils.filters import CallbackCommandFilter


@dp.callback_query_handler(CallbackCommandFilter(inline_commands.GET_SKIN_VIEW))
async def skin_view_callback(query: CallbackQuery):
    user = users[query.from_user.id]
    user.load_args_from_callback(query.data)
    bronoskin = BronoSkin.get_or_none(id=user["bronoskin_id"])
    if bronoskin:
        user.del_all_dialog_data()
        await query.answer()
        await query.message.reply(
            text=bronoskin.full_view(is_admin=user.is_admin(), recursive=2),
            reply_markup=inline_keyboards.bronoskin_view_actions(user=user, bronoskin=bronoskin))
    else:
        user.del_all_dialog_data()
        await query.answer(text=static.BRONOSKIN_NOT_EXIST, show_alert=True)


@dp.callback_query_handler(CallbackCommandFilter(inline_commands.GUARANTEE_BRONOSKIN))
async def create_guarantee_callback(query: CallbackQuery):
    user = users[query.from_user.id]
    user.load_args_from_callback(query.data)
    user["bronoskin"] = BronoSkin.get_or_none(id=user["bronoskin_id"])
    if not current_change.is_opened():
        user.del_all_dialog_data()
        await query.answer(text=static.OPEN_CHANGE_REQUIRED, show_alert=True)
    elif not user["bronoskin"]:
        user.del_all_dialog_data()
        await query.answer(text=static.BRONOSKIN_NOT_EXIST, show_alert=True)
    else:
        payment = user["bronoskin"].payment_set[0]
        if payment.refund_set:
            user.del_all_dialog_data()
            await query.answer(text=static.BRONOSKIN_ALREADY_REFUNDED, show_alert=True)
        elif payment.warranty_period < datetime.now():
            user.del_all_dialog_data()
            await query.answer(text=static.WARRANTY_WAS_EXPIRED, show_alert=True)
        else:
            user.state.jump(states.create_guarantee_group)
            await query.answer()
            await query.message.reply(
                text=dynamic.select_cut_variation_for_guarantee(user),
                reply_markup=reply_keyboards.select_cut_variation_for_guarantee(user))


@dp.callback_query_handler(CallbackCommandFilter(inline_commands.DELETE_BRONOSKIN))
async def delete_bronoskin_callback(query: CallbackQuery):
    user = users[query.from_user.id]
    user.load_args_from_callback(query.data)
    user["bronoskin"] = BronoSkin.get_or_none(id=user["bronoskin_id"])
    if not current_change.is_opened():
        user.del_all_dialog_data()
        await query.answer(text=static.OPEN_CHANGE_REQUIRED, show_alert=True)
    elif not user["bronoskin"]:
        user.del_all_dialog_data()
        await query.answer(text=static.BRONOSKIN_NOT_EXIST, show_alert=True)
    else:
        if datetime.now().date() == user["bronoskin"].datetime.date() or user.is_admin():
            user.state.set(states.DELETE_BRONOSKIN_CONFIRM)
            await query.answer()
            await query.message.reply(
                text=static.DELETE_BRONOSKIN_CONFIRM,
                reply_markup=CONFIRM_KEYBOARD)
        else:
            user.del_all_dialog_data()
            await query.answer(text=static.ACCESS_DENIED, show_alert=True)


@dp.callback_query_handler(CallbackCommandFilter(inline_commands.REFUND_BRONOSKIN))
async def refund_bronoskin_callback(query: CallbackQuery):
    user = users[query.from_user.id]
    user.load_args_from_callback(query.data)
    user["bronoskin"] = BronoSkin.get_or_none(id=user["bronoskin_id"])
    if not current_change.is_opened():
        user.del_all_dialog_data()
        await query.answer(text=static.OPEN_CHANGE_REQUIRED, show_alert=True)
    elif not user["bronoskin"]:
        user.del_all_dialog_data()
        await query.answer(text=static.BRONOSKIN_NOT_EXIST, show_alert=True)
    else:
        if user["bronoskin"].payment_set[0].refund_set:
            user.del_all_dialog_data()
            await query.answer(text=static.BRONOSKIN_ALREADY_REFUNDED, show_alert=True)
        else:
            user.state.jump(states.refund_bronoskin_group)
            await query.answer()
            await query.message.reply(
                text=static.REFUND_BRONOSKIN_COMMENT)


@dp.callback_query_handler(CallbackCommandFilter(inline_commands.ADD_COMMENT))
async def add_comment_callback(query: CallbackQuery):
    user = users[query.from_user.id]
    user.load_args_from_callback(query.data)
    user["bronoskin"] = BronoSkin.get_or_none(id=user["bronoskin_id"])
    if user["bronoskin"]:
        user.state.jump(states.new_comment_bronoskin_group)
        await query.answer()
        await query.message.reply(
            text=static.TYPE_BRONOSKIN_COMMENT)
    else:
        user.del_all_dialog_data()
        await query.answer(text=static.BRONOSKIN_NOT_EXIST, show_alert=True)
