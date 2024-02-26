import re

from aiogram import types
from aiogram.types import ReplyKeyboardRemove

import states.materials_command as states
import ui.keyboards.reply_keyboards.materials_command as reply_keyboards
from ui.keyboards import buttons_text
from ui.keyboards.reply_keyboards.misc import CONFIRM_KEYBOARD
from ui.text import static
import ui.text.dynamic.materials_command as dynamic

from loader import dp, users, current_change
from utils import views
from utils.database import MaterialsInventoryIntake, MaterialsInventoryOuttake
from utils.filters import StateFilter, AccessFilter
from utils.misc import REGEXP_FOR_SIZE, calculate_worksheet_count
from utils.rights import ACCESS_FOR_ALL, ACCESS_FOR_ADMINS
from utils.views import get_intake_by_id, check_intake_remains


@dp.message_handler(AccessFilter(*ACCESS_FOR_ALL), commands=['materials'])
async def process_materials_command(message: types.Message):
    user = users[message.from_user.id]
    user.del_all_dialog_data()
    user.state.set(states.SELECT_INVENT_ACTION)
    await message.reply(
        reply_markup=reply_keyboards.select_invent_action(user),
        text=dynamic.select_invent_action())


@dp.message_handler(StateFilter(states.SELECT_INVENT_ACTION), AccessFilter(*ACCESS_FOR_ALL))
async def select_invent_action_callback(message: types.Message):
    user = users[message.from_user.id]
    if message.text == buttons_text.OUTTAKE_MATERIALS:
        if current_change.is_opened() or user.is_admin():
            user.state.jump(states.materials_outtake_group)
            await message.reply(
                reply_markup=reply_keyboards.select_intake_id(),
                text=dynamic.material_incoming_list())
        else:
            await message.reply(
                text=static.OPEN_CHANGE_REQUIRED)
            await message.answer(
                reply_markup=reply_keyboards.select_invent_action(user),
                text=dynamic.select_invent_action())
    elif message.text == buttons_text.INTAKE_MATERIALS and user.is_admin():
        user.state.jump(states.materials_intake_group)
        await message.reply(
            reply_markup=reply_keyboards.get_material_types(),
            text=static.SELECT_MATERIAL_TYPE_FOR_INTAKE)
    else:
        await message.reply(
            text=static.INCORRECT_OPTION)
        await message.answer(
            reply_markup=reply_keyboards.select_invent_action(user),
            text=dynamic.select_invent_action())


@dp.message_handler(StateFilter(states.INVENTORIABLE_MATERIAL_TYPE_INTAKE), AccessFilter(*ACCESS_FOR_ADMINS))
async def inventoriable_material_line_callback(message: types.Message):
    material_type = views.get_material_type_by_name(message.text)
    user = users[message.from_user.id]
    if message.text == states.SELECT_INVENT_ACTION.back_button:
        user.state.prev()
        await message.reply(
            reply_markup=reply_keyboards.select_invent_action(user),
            text=dynamic.select_invent_action())
    elif not material_type:
        await message.reply(
            text=static.INCORRECT_OPTION)
        await message.reply(
            reply_markup=reply_keyboards.get_material_types(),
            text=static.SELECT_MATERIAL_TYPE_FOR_INTAKE)
    else:
        user["material_type"] = material_type
        user.state.next()
        await message.reply(
            reply_markup=reply_keyboards.MATERIAL_DIMENSION_TYPE,
            text=dynamic.select_dimension_type(user))


@dp.message_handler(StateFilter(states.MATERIAL_DIMENSION_TYPE), AccessFilter(*ACCESS_FOR_ADMINS))
async def material_dimension_callback(message: types.Message):
    user = users[message.from_user.id]
    if message.text == states.INVENTORIABLE_MATERIAL_TYPE_INTAKE.back_button:
        user.state.prev()
        del user["material_type"]
        await message.reply(
            reply_markup=reply_keyboards.get_material_types(),
            text=static.SELECT_MATERIAL_TYPE_FOR_INTAKE)
    elif message.text == buttons_text.ROLL_MATERIAL_TYPE:
        user.state.next()
        await message.reply(
            reply_markup=reply_keyboards.ROLL_DIMENSION,
            text=dynamic.type_roll_size(user))
    elif message.text == buttons_text.SHEET_MATERIAL_TYPE:
        user.state.set(states.SHEET_DIMENSION)
        await message.reply(
            reply_markup=reply_keyboards.sheet_dimension(user),
            text=dynamic.type_sheet_size(user))
    else:
        await message.reply(
            text=static.INCORRECT_OPTION)
        await message.answer(
            reply_markup=reply_keyboards.MATERIAL_DIMENSION_TYPE,
            text=dynamic.select_dimension_type(user))


@dp.message_handler(StateFilter(states.ROLL_DIMENSION), AccessFilter(*ACCESS_FOR_ADMINS))
async def roll_dimension_callback(message: types.Message):
    user = users[message.from_user.id]
    if message.text == states.MATERIAL_DIMENSION_TYPE.back_button:
        user.state.prev()
        await message.reply(
            reply_markup=reply_keyboards.MATERIAL_DIMENSION_TYPE,
            text=dynamic.select_dimension_type(user))
    elif re.match(REGEXP_FOR_SIZE, message.text):
        user["roll_size"] = [int(e) for e in message.text.split('*')]
        user.state.next()
        await message.reply(
            reply_markup=reply_keyboards.sheet_dimension(user),
            text=dynamic.type_sheet_size(user))
    else:
        await message.reply(
            text=static.INCORRECT_INPUT)
        await message.answer(
            reply_markup=reply_keyboards.ROLL_DIMENSION,
            text=dynamic.type_roll_size(user))


@dp.message_handler(StateFilter(states.SHEET_DIMENSION), AccessFilter(*ACCESS_FOR_ADMINS))
async def sheet_dimension_callback(message: types.Message):
    user = users[message.from_user.id]
    if message.text == states.ROLL_DIMENSION.back_button and user["roll_size"]:
        del user["roll_size"]
        user.state.prev()
        await message.reply(
            reply_markup=reply_keyboards.ROLL_DIMENSION,
            text=dynamic.type_roll_size(user))
    elif message.text == states.MATERIAL_DIMENSION_TYPE.back_button and not user["roll_size"]:
        user.state.set(states.MATERIAL_DIMENSION_TYPE)
        await message.reply(
            reply_markup=reply_keyboards.MATERIAL_DIMENSION_TYPE,
            text=dynamic.select_dimension_type(user))
    elif re.match(REGEXP_FOR_SIZE, message.text):
        user["sheet_size"] = [int(e) for e in message.text.split('*')]
        if user["roll_size"]:
            worksheet_count_per_roll = calculate_worksheet_count(*user["roll_size"], *user["sheet_size"])
            if worksheet_count_per_roll:
                user["worksheet_count_per_roll"] = worksheet_count_per_roll
                user.state.next()
                await message.reply(
                    reply_markup=reply_keyboards.MATERIAL_UNIT_COUNT,
                    text=dynamic.type_material_unit_count(user))
            else:
                del user["sheet_size"]
                await message.reply(
                    text=static.INCORRECT_WORKSHEET_SIZE)
                await message.answer(
                    reply_markup=reply_keyboards.sheet_dimension(user),
                    text=dynamic.type_sheet_size(user))
        else:
            user.state.next()
            await message.reply(
                reply_markup=reply_keyboards.MATERIAL_UNIT_COUNT,
                text=dynamic.type_material_unit_count(user))
    else:
        await message.reply(
            text=static.INCORRECT_INPUT)
        await message.answer(
            reply_markup=reply_keyboards.sheet_dimension(user),
            text=dynamic.type_sheet_size(user))


@dp.message_handler(StateFilter(states.MATERIAL_UNIT_COUNT), AccessFilter(*ACCESS_FOR_ADMINS))
async def material_unit_count_callback(message: types.Message):
    user = users[message.from_user.id]
    if message.text == states.SHEET_DIMENSION.back_button:
        del user["sheet_size"], user["worksheet_count_per_roll"]
        user.state.prev()
        await message.reply(
            reply_markup=reply_keyboards.sheet_dimension(user),
            text=dynamic.type_sheet_size(user))
    elif re.match(r"^[\d]+$", message.text):
        if user["roll_size"]:
            user["roll_count"] = int(message.text)
            user["total_worksheet_count"] = int(message.text) * user["worksheet_count_per_roll"]
        else:
            user["total_worksheet_count"] = int(message.text)
        user.state.next()
        await message.reply(
            reply_markup=reply_keyboards.MATERIAL_INTAKE_COST,
            text=dynamic.type_intake_cost(user))
    else:
        await message.reply(
            text=static.INCORRECT_OPTION)
        await message.answer(
            reply_markup=reply_keyboards.MATERIAL_UNIT_COUNT,
            text=dynamic.type_material_unit_count(user))


@dp.message_handler(StateFilter(states.MATERIAL_INTAKE_COST), AccessFilter(*ACCESS_FOR_ADMINS))
async def material_intake_cost_callback(message: types.Message):
    user = users[message.from_user.id]
    if message.text == states.MATERIAL_UNIT_COUNT.back_button:
        del user["roll_count"], user["total_worksheet_count"]
        user.state.prev()
        await message.reply(
            reply_markup=reply_keyboards.MATERIAL_UNIT_COUNT,
            text=dynamic.type_material_unit_count(user))
    elif re.match(r"^[\d]+$", message.text):
        user["total_cost"] = int(message.text)
        user["worksheet_cost"] = user["total_cost"] // user["total_worksheet_count"]
        user.state.next()
        await message.reply(
            reply_markup=CONFIRM_KEYBOARD,
            text=dynamic.material_intake_confirm(user))
    else:
        await message.reply(
            text=static.INCORRECT_OPTION)
        await message.answer(
            reply_markup=reply_keyboards.MATERIAL_INTAKE_COST,
            text=dynamic.type_intake_cost(user))


@dp.message_handler(StateFilter(states.MATERIAL_INTAKE_CONFIRM), AccessFilter(*ACCESS_FOR_ADMINS))
async def material_intake_confirm(message: types.Message):
    user = users[message.from_user.id]
    if message.text == buttons_text.OK:
        material_invent = MaterialsInventoryIntake.create(
            material_type=user["material_type"],
            size_x_cm=min(user["sheet_size"]),
            size_y_cm=max(user["sheet_size"]),
            worksheet_count=user["total_worksheet_count"],
            total_cost=user["total_cost"])
        user.state.finish()
        user.del_all_dialog_data()
        await message.reply(
            reply_markup=ReplyKeyboardRemove(),
            text=material_invent.full_view(is_admin=True))
    elif message.text == buttons_text.CANCEL:
        del user["total_cost"]
        user.state.prev()
        await message.reply(
            reply_markup=reply_keyboards.MATERIAL_INTAKE_COST,
            text=dynamic.type_intake_cost(user))
    else:
        await message.reply(
            text=static.INCORRECT_OPTION)
        await message.answer(
            reply_markup=CONFIRM_KEYBOARD,
            text=dynamic.material_intake_confirm(user))


@dp.message_handler(StateFilter(states.SELECT_INTAKE), AccessFilter(*ACCESS_FOR_ALL))
async def select_intake_callback(message: types.Message):
    user = users[message.from_user.id]
    if message.text == states.SELECT_INVENT_ACTION.back_button:
        user.state.prev()
        await message.reply(
            reply_markup=reply_keyboards.select_invent_action(user),
            text=dynamic.select_invent_action())
    elif re.match(r"^№[\d]+$", message.text):
        user["intake"] = get_intake_by_id(int(message.text.replace("№", "")))
        if user["intake"]:
            user.state.next()
            await message.reply(
                reply_markup=reply_keyboards.BACK_TO_SELECT_INTAKE,
                text=static.TYPE_OUTTAKE_COUNT)
        else:
            await message.reply(
                text=static.INTAKE_NOT_FOUND)
            await message.answer(
                reply_markup=reply_keyboards.select_intake_id(),
                text=dynamic.material_incoming_list())
    else:
        await message.reply(
            text=static.INCORRECT_INPUT)
        await message.answer(
            reply_markup=reply_keyboards.select_intake_id(),
            text=dynamic.material_incoming_list())


@dp.message_handler(StateFilter(states.MATERIAL_OUTTAKE_COUNT), AccessFilter(*ACCESS_FOR_ALL))
async def material_outtake_count_callback(message: types.Message):
    user = users[message.from_user.id]
    if message.text == states.SELECT_INTAKE.back_button:
        del user["intake"]
        user.state.prev()
        await message.reply(
            reply_markup=reply_keyboards.select_intake_id(),
            text=dynamic.material_incoming_list())
    elif re.match(r"^[\d]+$", message.text):
        outtake_count = int(message.text)
        if outtake_count == 0 or check_intake_remains(user["intake"]) - outtake_count < 0:
            await message.reply(
                text=static.INCORRECT_OUTTAKE_COUNT)
            await message.answer(
                reply_markup=reply_keyboards.BACK_TO_SELECT_INTAKE,
                text=static.TYPE_OUTTAKE_COUNT)
        else:
            user["outtake_count"] = outtake_count
            user.state.next()
            await message.reply(
                reply_markup=CONFIRM_KEYBOARD,
                text=dynamic.material_outtake_confirm(user))
    else:
        await message.reply(
            text=static.INCORRECT_INPUT)
        await message.answer(
            reply_markup=reply_keyboards.BACK_TO_SELECT_INTAKE,
            text=static.TYPE_OUTTAKE_COUNT)


@dp.message_handler(StateFilter(states.MATERIAL_OUTTAKE_CONFIRM), AccessFilter(*ACCESS_FOR_ALL))
async def material_outtake_confirm(message: types.Message):
    user = users[message.from_user.id]
    if message.text == buttons_text.OK:
        material_outtake = MaterialsInventoryOuttake.create(
            worker=user.im,
            intake=user["intake"],
            worksheet_count=user["outtake_count"])
        user.state.finish()
        user.del_all_dialog_data()
        await message.reply(
            reply_markup=ReplyKeyboardRemove(),
            text=material_outtake.full_view(is_admin=user.is_admin()))
    elif message.text == buttons_text.CANCEL:
        del user["outtake_count"]
        user.state.prev()
        await message.reply(
            reply_markup=reply_keyboards.BACK_TO_SELECT_INTAKE,
            text=static.TYPE_OUTTAKE_COUNT)
    else:
        await message.reply(
            text=static.INCORRECT_OPTION)
        await message.answer(
            reply_markup=CONFIRM_KEYBOARD,
            text=dynamic.material_outtake_confirm(user))
