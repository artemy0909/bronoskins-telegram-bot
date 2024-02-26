import os
import re

from aiogram import types
from aiogram.types import InputFile

import states.find_command as states
import ui.keyboards.reply_keyboards.find_command as reply_keyboards
from ui.keyboards.reply_keyboards.misc import CONFIRM_KEYBOARD
from ui.text import static
import ui.text.dynamic.find_command as dynamic
from ui.keyboards import buttons_text

from loader import dp, users
from utils import file_generators, views
from utils.filters import StateFilter, AccessFilter
from utils.misc import try_str_to_date_range, REGEXP_FOR_DEVICE_NAMES, REGEXP_FOR_STUFF_NAMES
from utils.rights import ACCESS_FOR_ALL
from utils.views import find_films

from ui.keyboards.inline_keyboards.bronoskin_actions import bronoskin_view_actions as keyboard_bronoskin_view_actions
from ui.keyboards.reply_keyboards.create_command import (get_payment_type_to_create
                                                         as keyboard_get_payment_type_to_create)


@dp.message_handler(AccessFilter(*ACCESS_FOR_ALL), commands=['find'])
async def process_create_command(message: types.Message):
    user = users[message.from_user.id]
    user.del_all_dialog_data()
    user.state.jump(states.films_line)
    await message.reply(
        reply_markup=reply_keyboards.films_signs(),
        text=static.FILMS_SIGNS)


@dp.message_handler(StateFilter(states.FILMS_SIGNS), AccessFilter(*ACCESS_FOR_ALL))
async def films_signs_callback(message: types.Message):
    user = users[message.from_user.id]

    async def basic_action():
        user.state.next()
        await message.reply(
            reply_markup=reply_keyboards.films_selections(user),
            text=dynamic.finder_films_args_info(user))

    if message.text == buttons_text.SKINS_WITH_PAYMENT:
        user["films_sign"] = "SKINS_WITH_PAYMENT"
        await basic_action()
    elif message.text == buttons_text.SKINS_WITH_WRITE_OFF:
        user["films_sign"] = "SKINS_WITH_WRITE_OFF"
        await basic_action()
    elif message.text == buttons_text.SKINS_WITHOUT_IMPLEMENTATION:
        user["films_sign"] = "SKINS_WITHOUT_IMPLEMENTATION"
        await basic_action()
    elif message.text == buttons_text.SKINS_WITH_GUARANTEE:
        user["films_sign"] = "SKINS_WITH_GUARANTEE"
        await basic_action()
    elif message.text == buttons_text.SKINS_WITH_REFUND:
        user["films_sign"] = "SKINS_WITH_REFUND"
        await basic_action()
    elif message.text == buttons_text.NOT_MATTER:
        user["films_sign"] = "NOT_MATTER"
        await basic_action()
    else:
        await message.reply(
            text=static.INCORRECT_OPTION)
        await message.answer(
            reply_markup=reply_keyboards.films_signs(),
            text=static.FILMS_SIGNS)


@dp.message_handler(StateFilter(states.FILMS_SELECTION), AccessFilter(*ACCESS_FOR_ALL))
async def films_selection_callback(message: types.Message):
    user = users[message.from_user.id]

    async def incorrect_option():
        await message.reply(
            text=static.INCORRECT_OPTION)
        await message.answer(
            reply_markup=reply_keyboards.films_selections(user),
            text=dynamic.finder_films_args_info(user))

    async def find_by_date(date_sign_label, selection_name):
        user.state.set(states.FIND_BY_DATE)
        user["date_sign_label"] = date_sign_label
        user["selection_name"] = selection_name
        await message.reply(
            text=dynamic.find_by_date_selection(user),
            reply_markup=reply_keyboards.BACK_TO_FILMS_SELECTION)

    async def find_by_stuff(stuff_sign_label, selection_name):
        user.state.set(states.FIND_BY_STUFF)
        user["stuff_sign_label"] = stuff_sign_label
        user["selection_name"] = selection_name
        await message.reply(
            text=dynamic.find_by_stuff_selection(user),
            reply_markup=reply_keyboards.get_stuff_to_find())

    if message.text == states.FILMS_SIGNS.back_button:
        user.state.prev()
        user.del_all_dialog_data()
        await message.reply(
            reply_markup=reply_keyboards.films_signs(),
            text=static.FILMS_SIGNS)
    elif message.text == buttons_text.START_SEARCHING:
        await message.reply(
            text=static.SEARCH_IN_PROCESS)
        user["results"] = find_films(user)
        if user["results"]:
            user.state.next()
            await message.answer(
                text=dynamic.find_results(len(user["results"])),
                reply_markup=CONFIRM_KEYBOARD)
        else:
            await message.answer(
                text=static.NOTHING_FOUNDED)
            await message.answer(
                reply_markup=reply_keyboards.films_selections(user),
                text=dynamic.finder_films_args_info(user))
    elif message.text == buttons_text.FIND_BY_DATE_CREATION:
        await find_by_date(date_sign_label="создания пленки", selection_name="find_by_date_creation")
    elif message.text == buttons_text.FIND_BY_DEVICE:
        user.state.set(states.FIND_BY_DEVICE)
        await message.reply(
            text=static.TYPE_DEVICE,
            reply_markup=reply_keyboards.BACK_TO_FILMS_SELECTION)
    elif message.text == buttons_text.FIND_BY_MATERIAL_TYPE:
        user.state.set(states.FIND_BY_MATERIAL_TYPE)
        await message.reply(
            text=static.SELECT_MATERIAL_TYPE_FOR_SEARCH,
            reply_markup=reply_keyboards.get_material_type_to_find())
    elif message.text == buttons_text.FIND_BY_CUT_TYPE:
        user.state.set(states.FIND_BY_CUT_TYPE)
        await message.reply(
            text=static.SELECT_CUT_TYPE_FOR_FIND,
            reply_markup=reply_keyboards.get_cut_type_to_find())
    elif message.text == buttons_text.FIND_BY_CREATION_WORKER:
        await find_by_stuff("создавшему пленку", "find_by_creation_worker")
    elif user["films_sign"] == "SKINS_WITH_PAYMENT" or user["films_sign"] == "SKINS_WITH_GUARANTEE" \
            or user["films_sign"] == "SKINS_WITH_REFUND":
        if message.text == buttons_text.FIND_BY_PAYMENT_WORKER:
            await find_by_stuff("продавшему пленку", "find_by_payment_worker")
        elif message.text == buttons_text.FIND_BY_PAYMENT_DATE:
            await find_by_date(date_sign_label="оплаты пленки", selection_name="find_by_date_payment")
        elif message.text == buttons_text.FIND_BY_PAYMENT_TYPE:
            user.state.set(states.FIND_BY_PAYMENT_TYPE)
            await message.reply(
                text=static.SELECT_PAYMENT_TYPE,
                reply_markup=reply_keyboards.get_payment_type_to_find())
        elif message.text == buttons_text.FIND_BY_MONEY_COUNT:
            user.state.set(states.FIND_BY_MONEY)
            await message.reply(
                text=static.TYPE_MONEY_COUNT,
                reply_markup=reply_keyboards.BACK_TO_FILMS_SELECTION)
        elif user["films_sign"] == "SKINS_WITH_GUARANTEE" and message.text == buttons_text.FIND_BY_GUARANTEE:
            await find_by_date(date_sign_label="гарантии", selection_name="find_by_date_guarantee")
        elif user["films_sign"] == "SKINS_WITH_REFUND" and message.text == buttons_text.FIND_BY_REFUND_DATE:
            await find_by_date(date_sign_label="возврата средств", selection_name="find_by_date_refund")
        elif user["films_sign"] == "SKINS_WITH_REFUND" and message.text == buttons_text.FIND_BY_REFUND_WORKER:
            await find_by_date(date_sign_label="вернувшему деньги", selection_name="find_by_refund_worker")
        else:
            await incorrect_option()
    elif user["films_sign"] == "SKINS_WITH_WRITE_OFF":
        if message.text == buttons_text.FIND_BY_WRITE_OFF_WORKER:
            await find_by_stuff("списавшему пленку", "find_by_write_off_worker")
        elif message.text == buttons_text.FIND_BY_WRITE_OFF_DATE:
            await find_by_date(date_sign_label="списания пленки", selection_name="find_by_date_write_off")
    else:
        await incorrect_option()


@dp.message_handler(StateFilter(states.FIND_BY_MONEY), AccessFilter(*ACCESS_FOR_ALL))
async def find_by_money_creation_callback(message: types.Message):
    user = users[message.from_user.id]
    if message.text == states.FILMS_SELECTION.back_button:
        user.state.set(states.FILMS_SELECTION)
        await message.reply(
            reply_markup=reply_keyboards.films_selections(user),
            text=dynamic.finder_films_args_info(user))
    elif re.match(r"[\d]+", message.text):
        user["find_by_money"] = int(message.text)
        user.state.set(states.FILMS_SELECTION)
        await message.reply(
            reply_markup=reply_keyboards.films_selections(user),
            text=dynamic.finder_films_args_info(user))
    else:
        await message.reply(
            text=static.INCORRECT_INPUT)
        await message.answer(
            text=dynamic.find_by_date_selection(user),
            reply_markup=reply_keyboards.BACK_TO_FILMS_SELECTION)


@dp.message_handler(StateFilter(states.FIND_BY_DATE), AccessFilter(*ACCESS_FOR_ALL))
async def find_by_date_creation_callback(message: types.Message):
    user = users[message.from_user.id]
    if message.text == states.FILMS_SELECTION.back_button:
        user.state.set(states.FILMS_SELECTION)
        await message.reply(
            reply_markup=reply_keyboards.films_selections(user),
            text=dynamic.finder_films_args_info(user))
    else:
        date_ = try_str_to_date_range(message.text)
        if date_:
            user[user["selection_name"]] = date_
            del user["selection_name"], user["date_sign_label"]
            user.state.set(states.FILMS_SELECTION)
            await message.reply(
                reply_markup=reply_keyboards.films_selections(user),
                text=dynamic.finder_films_args_info(user))
        else:
            await message.reply(
                text=static.INCORRECT_INPUT)
            await message.answer(
                text=dynamic.find_by_date_selection(user),
                reply_markup=reply_keyboards.BACK_TO_FILMS_SELECTION)


@dp.message_handler(StateFilter(states.FIND_BY_DEVICE), AccessFilter(*ACCESS_FOR_ALL))
async def find_by_device_callback(message: types.Message):
    user = users[message.from_user.id]
    if message.text == states.FILMS_SELECTION.back_button:
        user.state.set(states.FILMS_SELECTION)
        await message.reply(
            reply_markup=reply_keyboards.films_selections(user),
            text=dynamic.finder_films_args_info(user))
    elif re.match(REGEXP_FOR_DEVICE_NAMES, message.text):
        device = views.get_device_by_full_name(message.text)
        if not device:
            reply_keyboard, result = reply_keyboards.get_devices_to_find(message.text)
            if result:
                await message.reply(
                    reply_markup=reply_keyboard,
                    text=static.FINDER_TEXT)
            else:
                await message.reply(
                    reply_markup=reply_keyboard,
                    text=static.DEVICE_NOT_FOUND)
        else:
            user["find_by_device"] = device
            user.state.set(states.FILMS_SELECTION)
            await message.reply(
                reply_markup=reply_keyboards.films_selections(user),
                text=dynamic.finder_films_args_info(user))
    else:
        await message.reply(
            text=static.INCORRECT_SYMBOLS_USED)
        await message.answer(
            text=static.TYPE_DEVICE,
            reply_markup=reply_keyboards.BACK_TO_FILMS_SELECTION)


@dp.message_handler(StateFilter(states.FIND_BY_STUFF), AccessFilter(*ACCESS_FOR_ALL))
async def find_by_stuff_callback(message: types.Message):
    user = users[message.from_user.id]
    if message.text == states.FILMS_SELECTION.back_button:
        user.state.set(states.FILMS_SELECTION)
        await message.reply(
            reply_markup=reply_keyboards.films_selections(user),
            text=dynamic.finder_films_args_info(user))
    elif re.match(REGEXP_FOR_STUFF_NAMES, message.text):
        worker = views.get_stuff_by_full_name(message.text)
        if not worker:
            await message.reply(
                text=static.INCORRECT_USERNAME)
            await message.answer(
                text=dynamic.find_by_stuff_selection(user),
                reply_markup=reply_keyboards.get_stuff_to_find())
        else:
            user[user["selection_name"]] = worker
            del user["selection_name"], user["stuff_sign_label"]
            user.state.set(states.FILMS_SELECTION)
            await message.reply(
                reply_markup=reply_keyboards.films_selections(user),
                text=dynamic.finder_films_args_info(user))
    else:
        await message.reply(
            text=static.INCORRECT_SYMBOLS_USED)
        await message.reply(
            text=dynamic.find_by_stuff_selection(user),
            reply_markup=reply_keyboards.get_stuff_to_find())


@dp.message_handler(StateFilter(states.FIND_BY_PAYMENT_TYPE), AccessFilter(*ACCESS_FOR_ALL))
async def find_by_payment_type_callback(message: types.Message):
    user = users[message.from_user.id]
    if message.text == states.FILMS_SELECTION.back_button:
        user.state.set(states.FILMS_SELECTION)
        await message.reply(
            reply_markup=reply_keyboards.films_selections(user),
            text=dynamic.finder_films_args_info(user))
    else:
        payment_type = views.get_payment_type(message.text)
        if not payment_type:
            await message.reply(
                text=static.INCORRECT_OPTION)
            await message.answer(
                reply_markup=keyboard_get_payment_type_to_create(),
                text=dynamic.finder_films_args_info(user))
        else:
            user["find_by_payment_type"] = payment_type
            user.state.set(states.FILMS_SELECTION)
            await message.reply(
                reply_markup=reply_keyboards.films_selections(user),
                text=dynamic.finder_films_args_info(user))


@dp.message_handler(StateFilter(states.FIND_BY_CUT_TYPE), AccessFilter(*ACCESS_FOR_ALL))
async def find_by_cut_type_callback(message: types.Message):
    user = users[message.from_user.id]
    if message.text == states.FILMS_SELECTION.back_button:
        user.state.set(states.FILMS_SELECTION)
        await message.reply(
            reply_markup=reply_keyboards.films_selections(user),
            text=dynamic.finder_films_args_info(user))
    else:
        cut_type = views.get_cut_type_by_name(message.text)
        if not cut_type:
            await message.reply(
                text=static.INCORRECT_OPTION)
            await message.answer(
                text=static.SELECT_CUT_TYPE_FOR_FIND,
                reply_markup=reply_keyboards.get_cut_type_to_find())
        else:
            user["find_by_cut_type"] = cut_type
            user.state.set(states.FILMS_SELECTION)
            await message.reply(
                reply_markup=reply_keyboards.films_selections(user),
                text=dynamic.finder_films_args_info(user))


@dp.message_handler(StateFilter(states.FIND_BY_MATERIAL_TYPE), AccessFilter(*ACCESS_FOR_ALL))
async def find_by_material_type_callback(message: types.Message):
    user = users[message.from_user.id]
    if message.text == states.FILMS_SELECTION.back_button:
        user.state.set(states.FILMS_SELECTION)
        await message.reply(
            reply_markup=reply_keyboards.films_selections(user),
            text=dynamic.finder_films_args_info(user))
    else:
        material_type = views.get_material_type_by_name(message.text)
        if not material_type:
            await message.reply(
                text=static.INCORRECT_OPTION)
            await message.answer(
                text=static.SELECT_MATERIAL_TYPE_FOR_SEARCH,
                reply_markup=reply_keyboards.get_material_type_to_find())
        else:
            user["find_by_material_type"] = material_type
            user.state.set(states.FILMS_SELECTION)
            await message.reply(
                reply_markup=reply_keyboards.films_selections(user),
                text=dynamic.finder_films_args_info(user))


@dp.message_handler(StateFilter(states.FILMS_OUTPUT_RESULTS_CONFIRM), AccessFilter(*ACCESS_FOR_ALL))
async def films_output_results_confirm_callback(message: types.Message):
    user = users[message.from_user.id]
    if message.text == buttons_text.OK:
        user.state.finish()
        count = len(user["results"])
        if count <= 10:
            for skin in user["results"]:
                await message.answer(
                    reply_markup=keyboard_bronoskin_view_actions(user, skin),
                    text=skin.full_view(is_admin=user.is_admin(), recursive=1))
        else:
            await message.reply(
                text=static.PREPARING_FILE)
            file_path = file_generators.film_search_result_html(user["results"])
            await message.answer_document(InputFile(file_path, "Результат поиска.html"))
            os.remove(file_path)
        user.del_all_dialog_data()
    elif message.text == buttons_text.CANCEL:
        del user["results"]
        user.state.prev()
        await message.reply(
            reply_markup=reply_keyboards.films_selections(user),
            text=dynamic.finder_films_args_info(user))
    else:
        await message.reply(
            text=static.INCORRECT_OPTION)
        await message.answer(
            text=dynamic.find_results(len(user["results"])),
            reply_markup=CONFIRM_KEYBOARD)
