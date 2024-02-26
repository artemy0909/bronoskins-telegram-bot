import re
from datetime import datetime

from aiogram import types

import states.bronoskin_actions as states
import ui.keyboards.reply_keyboards.bronoskin_actions as reply_keyboards
import ui.keyboards.inline_keyboards.bronoskin_actions as inline_keyboards
from ui.keyboards import buttons_text
from ui.text import static
import ui.text.dynamic.bronoskin_actions as dynamic
from ui.keyboards.reply_keyboards.misc import CONFIRM_KEYBOARD

from loader import dp, users, current_change
from ui.keyboards import reply_keyboards
from utils import views
from utils.database import BronoSkin, Refund, SkinComment, Payment, Guarantee
from utils.filters import StateFilter, AccessFilter
from utils.rights import ACCESS_FOR_ALL
from utils.views import get_material_production_cost


@dp.message_handler(StateFilter(states.DELETE_BRONOSKIN_CONFIRM), AccessFilter(*ACCESS_FOR_ALL))
async def delete_bronoskin_confirm_callback(message: types.Message):
    user = users[message.from_user.id]
    if message.text == buttons_text.OK:
        user["bronoskin"].delete_instance(recursive=True)
        user.state.finish()
        user.del_all_dialog_data()
        await message.reply(
            text=static.DELETING_COMPLETED)
    elif message.text == buttons_text.CANCEL:
        user.state.finish()
        user.del_all_dialog_data()
        await message.answer(
            text=user["bronoskin"].full_view(is_admin=user.is_admin(), recursive=2),
            reply_markup=inline_keyboards.bronoskin_view_actions(user, user["bronoskin"]))
    else:
        await message.reply(
            text=static.INCORRECT_OPTION)
        await message.answer(
            text=static.DELETE_BRONOSKIN_CONFIRM,
            reply_markup=CONFIRM_KEYBOARD)


@dp.message_handler(StateFilter(states.BRONOSKIN_COMMENT), AccessFilter(*ACCESS_FOR_ALL))
async def new_bronoskin_comment_callback(message: types.Message):
    user = users[message.from_user.id]
    user["comment"] = message.text
    user.state.next()
    await message.reply(
        text=static.CONFIRM_SAVE_COMMENT,
        reply_markup=CONFIRM_KEYBOARD)


@dp.message_handler(StateFilter(states.NEW_COMMENT_BRONOSKIN_CONFIRM), AccessFilter(*ACCESS_FOR_ALL))
async def new_comment_bronoskin_confirm_callback(message: types.Message):
    user = users[message.from_user.id]
    if message.text == buttons_text.OK:
        SkinComment.create(
            skin=user["bronoskin"],
            worker=user.im,
            content=user["comment"])
        bronoskin = user["bronoskin"]
        user.state.finish()
        user.del_all_dialog_data()
        await message.reply(
            text=bronoskin.full_view(is_admin=user.is_admin(), recursive=2),
            reply_markup=inline_keyboards.bronoskin_view_actions(user, bronoskin))
    elif message.text == buttons_text.CANCEL:
        del user["comment"]
        user.state.prev()
        await message.reply(
            text=static.REFUND_BRONOSKIN_COMMENT)
    else:
        await message.reply(
            text=static.INCORRECT_OPTION)
        await message.answer(
            text=static.REFUND_BRONOSKIN_CONFIRM,
            reply_markup=CONFIRM_KEYBOARD)


@dp.message_handler(StateFilter(states.REFUND_BRONOSKIN_COMMENT), AccessFilter(*ACCESS_FOR_ALL))
async def refund_bronoskin_comment_callback(message: types.Message):
    user = users[message.from_user.id]
    user["comment"] = message.text
    user.state.next()
    await message.reply(
        text=static.REFUND_BRONOSKIN_CONFIRM,
        reply_markup=CONFIRM_KEYBOARD)


@dp.message_handler(StateFilter(states.REFUND_BRONOSKIN_CONFIRM), AccessFilter(*ACCESS_FOR_ALL))
async def refund_bronoskin_confirm_callback(message: types.Message):
    user = users[message.from_user.id]
    if message.text == buttons_text.OK:
        old_bronoskin = user["bronoskin"]
        payment = old_bronoskin.payment_set[0]
        Refund.create(
            payment=payment,
            worker=user.im,
            change=current_change.change)
        SkinComment.create(
            skin=old_bronoskin,
            worker=user.im,
            content=user["comment"])
        user.state.finish()
        user.del_all_dialog_data()
        await message.reply(
            text=old_bronoskin.full_view(is_admin=user.is_admin(), recursive=2),
            reply_markup=inline_keyboards.bronoskin_view_actions(user, old_bronoskin))
    elif message.text == buttons_text.CANCEL:
        del user["comment"]
        user.state.prev()
        await message.reply(
            text=static.REFUND_BRONOSKIN_COMMENT)
    else:
        await message.reply(
            text=static.INCORRECT_OPTION)
        await message.answer(
            text=static.REFUND_BRONOSKIN_CONFIRM,
            reply_markup=CONFIRM_KEYBOARD)


@dp.message_handler(StateFilter(states.SELECT_CUT_VARIATION_FOR_GUARANTEE), AccessFilter(*ACCESS_FOR_ALL))
async def select_cut_type_for_guarantee_callback(message: types.Message):
    user = users[message.from_user.id]
    cut_var = views.get_cut_var_by_name_n_device_type(message.text, user["bronoskin"].device.type)
    if not cut_var:
        await message.reply(
            text=static.INCORRECT_OPTION)
        await message.answer(
            text=dynamic.select_cut_variation_for_guarantee(user),
            reply_markup=reply_keyboards.select_cut_variation_for_guarantee(user))
    else:
        user["cut_variation"] = cut_var
        user.state.next()
        await message.reply(
            text=dynamic.select_material_type_for_guarantee(user),
            reply_markup=reply_keyboards.select_material(user))


@dp.message_handler(StateFilter(states.SELECT_MATERIAL_VARIATION_FOR_GUARANTEE), AccessFilter(*ACCESS_FOR_ALL))
async def select_material_variation_for_guarantee_callback(message: types.Message):
    material_variation = views.get_material_variation_by_name(message.text)
    user = users[message.from_user.id]
    if message.text == states.SELECT_CUT_VARIATION_FOR_GUARANTEE.back_button:
        del user["cut_variation"]
        user.state.prev()
        await message.reply(
            text=dynamic.select_cut_variation_for_guarantee(user),
            reply_markup=reply_keyboards.select_cut_variation_for_guarantee(user))
    elif not material_variation:
        await message.reply(
            text=static.INCORRECT_OPTION)
        await message.answer(
            text=dynamic.select_material_type_for_guarantee(user),
            reply_markup=reply_keyboards.select_material(user))
    else:
        user["material_variation"] = material_variation
        user["money"] = views.get_skin_price(user, guarantee=True)
        user.state.next()
        await message.reply(
            reply_markup=reply_keyboards.get_payment_type_to_guarantee(),
            text=dynamic.select_payment_type_for_guarantee(user))


@dp.message_handler(StateFilter(states.SELECT_PAYMENT_TYPE_FOR_GUARANTEE), AccessFilter(*ACCESS_FOR_ALL))
async def payment_type_line_callback(message: types.Message):
    user = users[message.from_user.id]

    async def cost_changed():
        if user["money"] < 0:
            user["money"] = views.get_skin_price(user)
            await message.reply(
                text=static.INCORRECT_COST)
            await message.answer(
                reply_markup=reply_keyboards.get_payment_type_to_guarantee(),
                text=dynamic.select_payment_type_for_guarantee(user))
        else:
            await message.reply(
                text=static.COST_CHANGED)
            await message.answer(
                reply_markup=reply_keyboards.get_payment_type_to_guarantee(),
                text=dynamic.select_payment_type_for_guarantee(user))

    if message.text == states.SELECT_MATERIAL_VARIATION_FOR_GUARANTEE.back_button:
        del user["money"], user["material_variation"]
        user.state.prev()
        await message.reply(
            text=dynamic.select_material_type_for_guarantee(user),
            reply_markup=reply_keyboards.select_material(user))
    elif re.match(r"^-?[\d]+$", message.text):
        user["money"] = int(message.text)
        await cost_changed()
    elif re.match(r"^-?[\d]+%$", message.text):
        base_cost = views.get_skin_price(user)
        user["money"] = int(base_cost - (base_cost * int(message.text.replace("%", "")) / 100))
        await cost_changed()
    else:
        payment_type = views.get_payment_type(message.text)
        if not payment_type:
            await message.reply(
                text=static.INCORRECT_OPTION)
            await message.answer(
                reply_markup=reply_keyboards.get_payment_type_to_guarantee(),
                text=dynamic.select_payment_type_for_guarantee(user))
        else:
            user["payment_type"] = payment_type
            user.state.next()
            await message.reply(
                reply_markup=CONFIRM_KEYBOARD,
                text=dynamic.confirm_guarantee_create(user))


@dp.message_handler(StateFilter(states.GUARANTEE_CREATE_CONFIRM), AccessFilter(*ACCESS_FOR_ALL))
async def guarantee_confirm_callback(message: types.Message):
    user = users[message.from_user.id]
    if message.text == buttons_text.OK:
        old_bronoskin = user["bronoskin"]
        bronoskin = BronoSkin.create(
            device=old_bronoskin.device,
            cut_variation=user["cut_variation"],
            res_cost=0,
            material_variation=user["material_variation"],
            change=current_change.change,
            res_count=0,
            material_cost=get_material_production_cost(user))
        old_payment = user["bronoskin"].payment_set[0]
        Payment.create(
            skin=bronoskin,
            money=user["money"],
            base_cost=views.get_skin_price(user, guarantee=True),
            payment_type=user["payment_type"],
            worker=user.im,
            change=current_change.change,
            client_number=old_payment.client_number,
            commission=user["payment_type"].commission,
            warranty_period=datetime.now(),
            worker_salary=views.get_worker_salary(user, guarantee=True))
        Guarantee.create(
            payment=old_payment,
            new_skin=bronoskin,
            worker=user.im,
            change=current_change.change)
        user.state.finish()
        user.del_all_dialog_data()
        await message.reply(
            text=old_bronoskin.full_view(is_admin=user.is_admin(), recursive=2),
            reply_markup=inline_keyboards.bronoskin_view_actions(user, old_bronoskin))
    elif message.text == buttons_text.CANCEL:
        user.state.prev()
        del user["payment_type"]
        await message.reply(
            reply_markup=reply_keyboards.get_payment_type_to_guarantee(),
            text=dynamic.select_payment_type_for_guarantee(user))
    else:
        await message.reply(
            text=static.INCORRECT_OPTION)
        await message.answer(
            reply_markup=CONFIRM_KEYBOARD,
            text=dynamic.guarantee_create_confirm(user))
