import datetime
import re

from aiogram import types
from aiogram.types import ReplyKeyboardRemove

import states.create_command as states
import ui.keyboards.reply_keyboards.create_command as reply_keyboards
import ui.keyboards.inline_keyboards.bronoskin_actions as inline_keyboards
from ui.keyboards import buttons_text
from ui.keyboards.reply_keyboards.misc import CONFIRM_KEYBOARD
import ui.text.dynamic.create_command as dynamic
from ui.text import static

import config
from loader import dp, users, current_change
from utils import views
from utils.database import DeviceBrand, Device, BronoSkin, Payment, WriteOff, DelayedSkin, SkinComment, Guarantee
from utils.filters import StateFilter, AccessFilter
from utils.misc import REGEXP_FOR_DEVICE_NAMES, ru_mobile_number_convert
from utils.rights import ACCESS_FOR_ALL
from utils.views import get_material_production_cost, get_worker_salary, get_res_production_cost


@dp.message_handler(AccessFilter(*ACCESS_FOR_ALL), commands=['create'])
async def process_create_command(message: types.Message):
    user = users[message.from_user.id]
    user.del_all_dialog_data()
    if current_change.is_opened():
        user.state.jump(states.create_bronoskin_group)
        await message.reply(
            reply_markup=ReplyKeyboardRemove(),
            text=static.NEW_CUT)
    else:
        await message.reply(
            text=static.OPEN_CHANGE_REQUIRED)


@dp.message_handler(StateFilter(states.DEVICE_LINE), AccessFilter(*ACCESS_FOR_ALL))
async def device_line_callback(message: types.Message):
    user = users[message.from_user.id]
    if message.text == buttons_text.CREATE_NEW_DEVICE:
        user.state.jump(states.device_create_group)
        await message.reply(
            reply_markup=reply_keyboards.BACK_TO_DEVICE_LINE,
            text=static.SELECT_BRAND)
    else:
        if re.match(REGEXP_FOR_DEVICE_NAMES, message.text):
            device = views.get_device_by_full_name(message.text)
            if not device:
                reply_keyboard, result = reply_keyboards.get_devices_to_create(message.text)
                if result:
                    await message.reply(
                        reply_markup=reply_keyboard,
                        text=static.FINDER_TEXT)
                else:
                    await message.reply(
                        reply_markup=reply_keyboard,
                        text=static.DEVICE_NOT_FOUND)
            else:
                user["device"] = device
                user.state.next()
                await message.reply(
                    reply_markup=reply_keyboards.get_cut_variations(user),
                    text=dynamic.select_cut_variation(user))
        else:
            await message.reply(
                text=static.INCORRECT_SYMBOLS_USED)
            await message.answer(
                reply_markup=ReplyKeyboardRemove(),
                text=static.NEW_CUT)


@dp.message_handler(StateFilter(states.BRAND_LINE), AccessFilter(*ACCESS_FOR_ALL))
async def brand_line_callback(message: types.Message):
    user = users[message.from_user.id]
    if message.text == states.DEVICE_LINE.back_button:
        user.del_all_dialog_data()
        user.state.prev()
        await message.reply(
            reply_markup=ReplyKeyboardRemove(),
            text=static.NEW_CUT)
    elif message.text == buttons_text.CREATE_NEW_BRAND:
        user.state.jump(states.brand_create_group)
        await message.reply(
            reply_markup=reply_keyboards.BACK_TO_BRAND_LINE,
            text=static.NEW_BRAND)
    elif re.match(REGEXP_FOR_DEVICE_NAMES, message.text):
        brand = views.get_brand_by_name(message.text)
        if not brand:
            reply_keyboard, result = reply_keyboards.get_brand_to_create(message.text)
            if result:
                await message.reply(
                    reply_markup=reply_keyboard,
                    text=static.FINDER_TEXT)
            else:
                await message.reply(
                    reply_markup=reply_keyboard,
                    text=static.DEVICE_NOT_FOUND)
        else:
            user["brand"] = brand
            user.state.next()
            await message.reply(
                reply_markup=reply_keyboards.BACK_TO_BRAND_LINE,
                text=dynamic.device_create(user))
    else:
        await message.reply(
            text=static.INCORRECT_SYMBOLS_USED)
        await message.answer(
            reply_markup=reply_keyboards.BACK_TO_DEVICE_LINE,
            text=static.SELECT_BRAND)


@dp.message_handler(StateFilter(states.BRAND_CREATE), AccessFilter(*ACCESS_FOR_ALL))
async def brand_create_callback(message: types.Message):
    user = users[message.from_user.id]
    if message.text == states.BRAND_LINE.back_button:
        user.state.prev()
        await message.reply(
            reply_markup=reply_keyboards.BACK_TO_DEVICE_LINE,
            text=static.SELECT_BRAND)
    else:
        if not views.check_brand_exist(message.text):
            if re.match(REGEXP_FOR_DEVICE_NAMES, message.text):
                user["brand_name"] = message.text
                user.state.next()
                await message.reply(
                    reply_markup=CONFIRM_KEYBOARD,
                    text=dynamic.brand_create_confirm(user))
            else:
                await message.reply(
                    text=static.ILLEGAL_SYMBOLS_PASTED)
                await message.answer(
                    reply_markup=reply_keyboards.BACK_TO_BRAND_LINE,
                    text=static.NEW_BRAND)
        else:
            await message.reply(
                text=static.BRAND_ALREADY_EXISTS)
            await message.answer(
                reply_markup=reply_keyboards.BACK_TO_BRAND_LINE,
                text=static.NEW_BRAND)


@dp.message_handler(StateFilter(states.BRAND_CREATE_CONFIRM), AccessFilter(*ACCESS_FOR_ALL))
async def brand_create_confirm_callback(message: types.Message):
    user = users[message.from_user.id]
    if message.text == buttons_text.OK:
        user["brand"] = DeviceBrand.create(name=user["brand_name"])
        user.state.finish()
        del user["brand_name"]
        await message.reply(
            reply_markup=reply_keyboards.BACK_TO_BRAND_LINE,
            text=dynamic.device_create(user))
    elif message.text == buttons_text.CANCEL:
        del user["brand_name"]
        user.state.prev()
        await message.reply(
            reply_markup=reply_keyboards.BACK_TO_BRAND_LINE,
            text=static.NEW_BRAND)
    else:
        await message.reply(
            text=static.INCORRECT_OPTION)
        await message.answer(
            reply_markup=CONFIRM_KEYBOARD,
            text=dynamic.brand_create_confirm(user))


@dp.message_handler(StateFilter(states.DEVICE_CREATE), AccessFilter(*ACCESS_FOR_ALL))
async def device_create_callback(message: types.Message):
    user = users[message.from_user.id]
    if message.text == states.BRAND_LINE.back_button:
        del user["brand"]
        user.state.prev()
        await message.reply(
            reply_markup=reply_keyboards.BACK_TO_DEVICE_LINE,
            text=static.SELECT_BRAND)
    else:
        if not views.check_device_exist(user["brand"], message.text):
            if re.match(REGEXP_FOR_DEVICE_NAMES, message.text):
                if user["brand"].name in message.text:
                    await message.reply(
                        text=static.DEVICE_NAME_CONTAINS_BRAND)
                    await message.answer(
                        reply_markup=reply_keyboards.BACK_TO_BRAND_LINE,
                        text=dynamic.device_create(user))
                else:
                    user["device_name"] = message.text
                    user.state.next()
                    await message.reply(
                        reply_markup=reply_keyboards.get_device_type(),
                        text=dynamic.select_device_type(user))
            else:
                await message.reply(
                    text=static.ILLEGAL_SYMBOLS_PASTED)
                await message.answer(
                    reply_markup=reply_keyboards.BACK_TO_BRAND_LINE,
                    text=dynamic.device_create(user))
        else:
            await message.reply(
                text=static.DEVICE_ALREADY_EXISTS)
            await message.answer(
                reply_markup=reply_keyboards.BACK_TO_BRAND_LINE,
                text=dynamic.device_create(user))


@dp.message_handler(StateFilter(states.DEVICE_TYPE_LINE), AccessFilter(*ACCESS_FOR_ALL))
async def device_type_line_callback(message: types.Message):
    user = users[message.from_user.id]
    if message.text == states.DEVICE_CREATE.back_button:
        del user["device_name"]
        user.state.prev()
        await message.reply(
            reply_markup=reply_keyboards.BACK_TO_BRAND_LINE,
            text=dynamic.device_create(user))
    else:
        device_type = views.get_device_type_by_name(message.text)
        if not device_type:
            await message.reply(
                text=static.INCORRECT_OPTION)
            await message.answer(
                reply_markup=reply_keyboards.get_device_type(),
                text=dynamic.select_device_type(user))
        else:
            user["device_type"] = device_type
            user.state.next()
            await message.reply(
                reply_markup=CONFIRM_KEYBOARD,
                text=dynamic.device_create_confirm(user))


@dp.message_handler(StateFilter(states.DEVICE_CREATE_CONFIRM), AccessFilter(*ACCESS_FOR_ALL))
async def device_create_confirm_callback(message: types.Message):
    user = users[message.from_user.id]
    if message.text == buttons_text.OK:
        user["device"] = Device.create(brand=user["brand"], name=user["device_name"], type=user["device_type"])
        user.state.finish()
        del user["device_name"], user["device_type"]
        await message.reply(
            reply_markup=reply_keyboards.get_cut_variations(user),
            text=dynamic.select_cut_variation(user))
    elif message.text == buttons_text.CANCEL:
        del user["device_type"]
        user.state.prev()
        await message.answer(
            reply_markup=reply_keyboards.get_device_type(),
            text=dynamic.select_device_type(user))
    else:
        await message.reply(
            text=static.INCORRECT_OPTION)
        await message.reply(
            reply_markup=reply_keyboards.BACK_TO_BRAND_LINE,
            text=dynamic.device_create(user))


@dp.message_handler(StateFilter(states.CUT_VARIATION_LINE), AccessFilter(*ACCESS_FOR_ALL))
async def cut_variation_line_callback(message: types.Message):
    user = users[message.from_user.id]
    if message.text == states.DEVICE_LINE.back_button:
        user.del_all_dialog_data()
        user.state.prev()
        await message.reply(
            reply_markup=ReplyKeyboardRemove(),
            text=static.NEW_CUT)
    elif message.text == buttons_text.SHORT_CUT:
        if user["device"].type.name in ["Смартфон", "Планшет", "Смартчасы"]:
            user["cut_variation"] = views.get_cut_var_by_name_n_device_type("Экран", user["device"].type)
            user["material_variation"] = views.get_material_variation_by_name("Глянцевая")
            user["money"] = views.get_skin_price(user, False)
            user.state.set(states.PAYMENT_TYPE_LINE)
            await message.reply(
                reply_markup=reply_keyboards.get_payment_type_to_create(),
                text=dynamic.select_payment_type(user))
        else:
            await message.reply(
                text=static.SHORTCUT_INCORRECT)
            await message.answer(
                reply_markup=reply_keyboards.get_cut_variations(user),
                text=dynamic.select_cut_variation(user))
    else:
        cut_var = views.get_cut_var_by_name_n_device_type(message.text, user["device"].type)
        if not cut_var:
            await message.reply(
                text=static.INCORRECT_OPTION)
            await message.answer(
                reply_markup=reply_keyboards.get_cut_variations(user),
                text=dynamic.select_cut_variation(user))
        else:
            user["cut_variation"] = cut_var
            user.state.next()
            await message.reply(
                reply_markup=reply_keyboards.get_material_variation(user),
                text=dynamic.select_material(user))


@dp.message_handler(StateFilter(states.MATERIAL_VARIATION_LINE), AccessFilter(*ACCESS_FOR_ALL))
async def material_variation_line_callback(message: types.Message):
    user = users[message.from_user.id]
    if message.text == states.CUT_VARIATION_LINE.back_button:
        del user["cut_variation"]
        user.state.prev()
        await message.reply(
            reply_markup=reply_keyboards.get_cut_variations(user),
            text=dynamic.select_cut_variation(user))
    else:
        material_variation = views.get_material_variation_by_name(message.text)
        if not material_variation:
            await message.reply(
                text=static.INCORRECT_OPTION)
            await message.answer(
                reply_markup=reply_keyboards.get_material_variation(user),
                text=dynamic.select_material(user))
        else:
            user["material_variation"] = material_variation
            user.state.next()
            await message.reply(
                reply_markup=reply_keyboards.proceed_bronoskin(user),
                text=dynamic.select_implementation(user))


@dp.message_handler(StateFilter(states.PROCEED_BRONOSKIN), AccessFilter(*ACCESS_FOR_ALL))
async def proceed_bronoskin_callback(message: types.Message):
    user = users[message.from_user.id]
    if message.text == states.MATERIAL_VARIATION_LINE.back_button:
        del user["material_variation"]
        user.state.prev()
        await message.reply(
            reply_markup=reply_keyboards.get_material_variation(user),
            text=dynamic.select_material(user))
    elif message.text == buttons_text.GET_PAYMENT:
        user.state.next()
        user["money"] = views.get_skin_price(user, user["guarantee"])
        await message.reply(
            reply_markup=reply_keyboards.get_payment_type_to_create(),
            text=dynamic.select_payment_type(user))
    elif message.text == buttons_text.DELAYED_IMPLEMENTATION:
        if "comment" in user:
            user.state.jump(states.delayed_implementation_confirm_group)
            await message.reply(
                reply_markup=CONFIRM_KEYBOARD,
                text=dynamic.delayed_payment_create_confirm(user))
        else:
            await message.reply(
                text=static.COMMENT_REQUIRED)
            await message.answer(
                reply_markup=reply_keyboards.proceed_bronoskin(user),
                text=dynamic.select_implementation(user))
    elif message.text == buttons_text.WRITE_OFF_SKIN:
        if "comment" in user:
            user.state.jump(states.write_off_confirm_group)
            await message.reply(
                reply_markup=reply_keyboards.YN_KEYBOARD,
                text=dynamic.select_is_material_ruined(user))
        else:
            await message.reply(
                text=static.COMMENT_REQUIRED)
            await message.answer(
                reply_markup=reply_keyboards.proceed_bronoskin(user),
                text=dynamic.select_implementation(user))
    elif message.text == buttons_text.GUARANTEE_BRONOSKIN:
        user.state.next()
        user["guarantee"] = True
        await message.reply(
            reply_markup=reply_keyboards.get_payment_type_to_create(),
            text=dynamic.select_payment_type(user))
    elif len(message.text) > 1024:
        await message.reply(
            text=static.COMMENT_TOO_LONG)
        await message.answer(
            reply_markup=reply_keyboards.proceed_bronoskin(user),
            text=dynamic.select_implementation(user))
    else:
        if "comment" in user:
            if message.text == buttons_text.DELETE_COMMENT:
                del user["comment"]
                await message.reply(
                    text=static.COMMENT_DELETED)
            else:
                user["comment"] = message.text
                await message.reply(
                    text=static.COMMENT_CHANGED)
        else:
            user["comment"] = message.text
            await message.reply(
                text=static.COMMENT_ADDED)
        await message.answer(
            reply_markup=reply_keyboards.proceed_bronoskin(user),
            text=dynamic.select_implementation(user))


# @dp.message_handler(StateFilter(states.CLIENT_NUMBER), AccessFilter(*ACCESS_FOR_ALL))
# async def client_number_callback(message: types.Message):
#     user = users[message.from_user.id]
#     number = ru_mobile_number_convert(message.text)
#     if message.text == states.PROCEED_BRONOSKIN.back_button:
#         user.state.prev()
#         await message.reply(
#             reply_markup=reply_keyboards.proceed_bronoskin(user),
#             text=dynamic.select_implementation(user))
#     elif message.text == buttons_text.SKIP:
#         user["money"] = views.get_skin_price(user, user["guarantee"])
#         user.state.next()
#         await message.reply(
#             reply_markup=reply_keyboards.get_payment_type_to_create(),
#             text=dynamic.select_payment_type(user))
#     elif number:
#         user["number"] = number
#         user["money"] = views.get_skin_price(user, user["guarantee"])
#         user.state.next()
#         await message.reply(
#             reply_markup=reply_keyboards.get_payment_type_to_create(),
#             text=dynamic.select_payment_type(user))
#     else:
#         await message.reply(
#             text=static.INCORRECT_INPUT)
#         await message.answer(
#             reply_markup=reply_keyboards.TYPE_CLIENT_NUMBER,
#             text=dynamic.type_client_number(user))


@dp.message_handler(StateFilter(states.PAYMENT_TYPE_LINE), AccessFilter(*ACCESS_FOR_ALL))
async def payment_type_line_callback(message: types.Message):
    user = users[message.from_user.id]

    async def cost_changed():
        if user["money"] < 0:
            user["money"] = views.get_skin_price(user, user["guarantee"])
            await message.reply(
                text=static.INCORRECT_COST)
            await message.answer(
                reply_markup=reply_keyboards.get_payment_type_to_create(),
                text=dynamic.select_payment_type(user))
        else:
            await message.reply(
                text=static.COST_CHANGED)
            await message.answer(
                reply_markup=reply_keyboards.get_payment_type_to_create(),
                text=dynamic.select_payment_type(user))

    if message.text == states.PROCEED_BRONOSKIN.back_button:
        del user["money"], user["number"], user["guarantee"]
        user.state.prev()
        # await message.reply(
        #     reply_markup=reply_keyboards.TYPE_CLIENT_NUMBER,
        #     text=dynamic.type_client_number(user))
        await message.reply(
            reply_markup=reply_keyboards.proceed_bronoskin(user),
            text=dynamic.select_implementation(user))
    elif re.match(r"^-?\d+$", message.text):
        user["money"] = int(message.text)
        await cost_changed()
    elif re.match(r"^-?\d+%$", message.text):
        base_cost = views.get_skin_price(user)
        user["money"] = int(base_cost - (base_cost * int(message.text.replace("%", "")) / 100))
        await cost_changed()
    else:
        payment_type = views.get_payment_type(message.text)
        if not payment_type:
            await message.reply(
                text=static.INCORRECT_OPTION)
            await message.answer(
                reply_markup=reply_keyboards.get_payment_type_to_create(),
                text=dynamic.select_payment_type(user))
        else:
            user["payment_type"] = payment_type
            user.state.next()
            await message.reply(
                reply_markup=CONFIRM_KEYBOARD,
                text=dynamic.bronoskin_create_confirm(user))


@dp.message_handler(StateFilter(states.BRONOSKIN_CONFIRM), AccessFilter(*ACCESS_FOR_ALL))
async def bronoskin_confirm_callback(message: types.Message):
    user = users[message.from_user.id]
    if message.text == buttons_text.OK:
        bronoskin = BronoSkin.create(
            device=user["device"],
            cut_variation=user["cut_variation"],
            material_variation=user["material_variation"],
            res_cost=0 if user["guarantee"] else get_res_production_cost(user),
            change=current_change.change,
            res_count=0 if user["guarantee"] else user["cut_variation"].cut_type.res_count,
            material_cost=get_material_production_cost(user))
        if user["guarantee"]:
            Guarantee.create(
                new_skin=bronoskin,
                worker=user.im,
                change=current_change.change)
        Payment.create(
            skin=bronoskin,
            money=user["money"],
            base_cost=views.get_skin_price(user, user["guarantee"]),
            payment_type=user["payment_type"],
            worker=user.im,
            client_number=user["number"],
            commission=user["payment_type"].commission, change=current_change.change,
            warranty_period=datetime.datetime.now() if user["guarantee"] else
            datetime.datetime.now() + datetime.timedelta(days=config.WARRANTY_DAYS),
            worker_salary=get_worker_salary(user, user["guarantee"]))
        if user["comment"]:
            SkinComment.create(skin=bronoskin, worker=user.im, content=user["comment"])
        user.state.finish()
        user.del_all_dialog_data()
        await message.reply(
            reply_markup=inline_keyboards.bronoskin_view_actions(user, bronoskin),
            text=bronoskin.full_view(is_admin=user.is_admin(), recursive=1))
    elif message.text == buttons_text.CANCEL:
        user.state.prev()
        del user["payment_type"]
        await message.reply(
            reply_markup=reply_keyboards.get_payment_type_to_create(),
            text=dynamic.select_payment_type(user))
    else:
        await message.reply(
            text=static.INCORRECT_OPTION)
        await message.answer(
            reply_markup=CONFIRM_KEYBOARD,
            text=dynamic.bronoskin_create_confirm(user))


@dp.message_handler(StateFilter(states.WRITE_OFF_IS_MATERIAL_RUINED), AccessFilter(*ACCESS_FOR_ALL))
async def write_off_is_material_ruined_callback(message: types.Message):
    user = users[message.from_user.id]
    if message.text == states.PROCEED_BRONOSKIN.back_button:
        user.state.prev()
        await message.reply(
            reply_markup=reply_keyboards.proceed_bronoskin(user),
            text=dynamic.select_implementation(user))
    elif message.text == buttons_text.YES:
        user.state.next()
        user["is_material_ruined"] = True
        await message.reply(
            reply_markup=CONFIRM_KEYBOARD,
            text=dynamic.write_off_confirm(user))
    elif message.text == buttons_text.NO:
        user.state.next()
        user["is_material_ruined"] = False
        await message.reply(
            reply_markup=CONFIRM_KEYBOARD,
            text=dynamic.write_off_confirm(user))
    else:
        await message.reply(
            text=static.INCORRECT_OPTION)
        await message.reply(
            reply_markup=reply_keyboards.YN_KEYBOARD,
            text=dynamic.select_is_material_ruined(user))


@dp.message_handler(StateFilter(states.WRITE_OFF_CONFIRM), AccessFilter(*ACCESS_FOR_ALL))
async def write_off_confirm_callback(message: types.Message):
    user = users[message.from_user.id]
    if message.text == buttons_text.OK:
        bronoskin = BronoSkin.create(
            device=user["device"],
            cut_variation=user["cut_variation"],
            material_variation=user["material_variation"],
            res_count=user["cut_variation"].cut_type.res_count,
            res_cost=get_res_production_cost(user),
            change=current_change.change,
            material_cost=get_material_production_cost(user) if user["is_material_ruined"] else 0)
        WriteOff.create(
            skin=bronoskin,
            worker=user.im,
            change=current_change.change,
            is_material_ruined=user["is_material_ruined"])
        SkinComment.create(
            skin=bronoskin,
            worker=user.im,
            content=user["comment"])
        user.state.finish()
        user.del_all_dialog_data()
        await message.reply(
            reply_markup=inline_keyboards.bronoskin_view_actions(user, bronoskin),
            text=bronoskin.full_view(is_admin=user.is_admin(), recursive=1))
    elif message.text == buttons_text.CANCEL:
        user.state.prev()
        await message.reply(
            reply_markup=reply_keyboards.YN_KEYBOARD,
            text=dynamic.select_is_material_ruined(user))
    else:
        await message.reply(
            text=static.INCORRECT_OPTION)
        await message.answer(
            reply_markup=CONFIRM_KEYBOARD,
            text=dynamic.write_off_confirm(user))


@dp.message_handler(StateFilter(states.WRITE_OFF_CONFIRM), AccessFilter(*ACCESS_FOR_ALL))
async def write_off_confirm_callback(message: types.Message):
    user = users[message.from_user.id]
    if message.text == buttons_text.OK:
        bronoskin = BronoSkin.create(
            device=user["device"],
            cut_variation=user["cut_variation"],
            material_variation=user["material_variation"],
            res_count=user["cut_variation"].cut_type.res_count,
            res_cost=get_res_production_cost(user),
            change=current_change.change,
            material_cost=get_material_production_cost(user) if user["is_material_ruined"] else 0)
        WriteOff.create(
            skin=bronoskin,
            worker=user.im,
            change=current_change.change,
            is_material_ruined=user["is_material_ruined"])
        SkinComment.create(
            skin=bronoskin,
            worker=user.im,
            content=user["comment"])
        user.state.finish()
        user.del_all_dialog_data()
        await message.reply(
            reply_markup=inline_keyboards.bronoskin_view_actions(user, bronoskin),
            text=bronoskin.full_view(is_admin=user.is_admin(), recursive=1))
    elif message.text == buttons_text.CANCEL:
        user.state.prev()
        del user["is_material_ruined"]
        await message.reply(
            reply_markup=reply_keyboards.proceed_bronoskin(user),
            text=dynamic.select_implementation(user))
    else:
        await message.reply(
            text=static.INCORRECT_OPTION)
        await message.answer(
            reply_markup=CONFIRM_KEYBOARD,
            text=dynamic.write_off_confirm(user))


@dp.message_handler(StateFilter(states.DELAYED_IMPLEMENTATION_CONFIRM), AccessFilter(*ACCESS_FOR_ALL))
async def delayed_implementation_confirm_callback(message: types.Message):
    user = users[message.from_user.id]
    if message.text == buttons_text.OK:
        bronoskin = BronoSkin.create(
            device=user["device"],
            cut_variation=user["cut_variation"],
            material_variation=user["material_variation"],
            res_count=user["cut_variation"].cut_type.res_count,
            res_cost=get_res_production_cost(user),
            change=current_change.change,
            material_cost=get_material_production_cost(user))
        DelayedSkin.create(
            skin=bronoskin,
            worker=user.im,
            change=current_change.change)
        SkinComment.create(
            skin=bronoskin,
            worker=user.im,
            content=user["comment"])
        user.state.finish()
        user.del_all_dialog_data()
        await message.reply(
            reply_markup=inline_keyboards.bronoskin_view_actions(user, bronoskin),
            text=bronoskin.full_view(is_admin=user.is_admin(), recursive=1))
    elif message.text == buttons_text.CANCEL:
        user.state.prev()
        await message.reply(
            reply_markup=reply_keyboards.proceed_bronoskin(user),
            text=dynamic.select_implementation(user))
    else:
        await message.reply(
            text=static.INCORRECT_OPTION)
        await message.answer(
            reply_markup=CONFIRM_KEYBOARD,
            text=dynamic.delayed_payment_create_confirm(user))
