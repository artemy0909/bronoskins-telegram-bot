from aiogram.types import ReplyKeyboardMarkup

import states.find_command as states
from ui.keyboards import buttons_text
from ui.keyboards.reply_keyboards._generators import _linear_generator, _fuzzy_device, _all_users
from utils.database import PaymentType, CutType, MaterialType
from utils.manager import User

BACK_TO_FILMS_SELECTION = _linear_generator([states.FILMS_SELECTION.back_button])


def finder_select() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    keyboard.add(buttons_text.SKINS)
    keyboard.add(buttons_text.DEVICES)
    keyboard.add(buttons_text.INVENT)
    return keyboard


def films_signs() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    keyboard.add(buttons_text.SKINS_WITH_PAYMENT)
    keyboard.add(buttons_text.SKINS_WITH_WRITE_OFF)
    keyboard.add(buttons_text.SKINS_WITHOUT_IMPLEMENTATION)
    keyboard.add(buttons_text.SKINS_WITH_GUARANTEE)
    keyboard.add(buttons_text.SKINS_WITH_REFUND)
    keyboard.add(buttons_text.NOT_MATTER)
    return keyboard


def films_selections(user: User) -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    keyboard.add(states.FILMS_SIGNS.back_button)
    keyboard.add(buttons_text.START_SEARCHING)
    if user["films_sign"] == "NOT_MATTER" or user["films_sign"] == "SKINS_WITHOUT_IMPLEMENTATION":
        for e in buttons_text.not_matter_sign_button_set:
            keyboard.add(e)
    elif user["films_sign"] == "SKINS_WITH_PAYMENT":
        for e in buttons_text.payment_sign_button_set:
            keyboard.add(e)
    elif user["films_sign"] == "SKINS_WITH_WRITE_OFF":
        for e in buttons_text.write_off_sign_button_set:
            keyboard.add(e)
    elif user["films_sign"] == "SKINS_WITH_GUARANTEE":
        for e in buttons_text.guarantee_sign_button_set:
            keyboard.add(e)
    elif user["films_sign"] == "SKINS_WITH_REFUND":
        for e in buttons_text.refund_sign_button_set:
            keyboard.add(e)
    else:
        raise ValueError
    return keyboard


def get_devices_to_find(user_text: str) -> tuple[ReplyKeyboardMarkup, bool]:
    keyboard = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    keyboard.add(states.FILMS_SELECTION.back_button)
    fuzzy = _fuzzy_device(user_text)
    for device in fuzzy:
        keyboard.add(device)
    result = True if fuzzy else False
    return keyboard, result


def get_stuff_to_find() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    keyboard.add(states.FILMS_SELECTION.back_button)
    for username in _all_users():
        keyboard.add(username)
    return keyboard


def get_payment_type_to_find() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    keyboard.add(states.FILMS_SELECTION.back_button)
    for payment_type in PaymentType.select():
        keyboard.add(payment_type.button)
    return keyboard


def get_cut_type_to_find() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    keyboard.add(states.FILMS_SELECTION.back_button)
    for cut_type in CutType.select():
        keyboard.add(cut_type.name)
    return keyboard


def get_material_type_to_find() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    keyboard.add(states.FILMS_SELECTION.back_button)
    for material_type in MaterialType.select():
        keyboard.add(material_type.name)
    return keyboard
