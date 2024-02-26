from aiogram.types import ReplyKeyboardMarkup

import states.create_command as states
from ui.keyboards import buttons_text
from ._generators import _linear_generator, _fuzzy_device, _fuzzy_brand
from utils.database import DeviceType, PaymentType, CutVariation
from utils.manager import User
import config
BACK_TO_DEVICE_LINE = _linear_generator([states.DEVICE_LINE.back_button])
BACK_TO_BRAND_LINE = _linear_generator([states.BRAND_LINE.back_button])
TYPE_CLIENT_NUMBER = _linear_generator([states.PROCEED_BRONOSKIN.back_button, buttons_text.SKIP])
YN_KEYBOARD = \
    ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True) \
    .add(states.PROCEED_BRONOSKIN.back_button).row(buttons_text.YES, buttons_text.NO)


def get_material_variation(user: User) -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    keyboard.add(states.CUT_VARIATION_LINE.back_button)
    for price in user["cut_variation"].pricelist_set:
        keyboard.add(price.material_variation.name)
    return keyboard


def get_cut_variations(user: User) -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    keyboard.add(states.DEVICE_LINE.back_button)
    if config.CREATE_SHORT_CUT_BUTTON:
        keyboard.add(buttons_text.SHORT_CUT)
    for cut_variation in CutVariation.select().where(CutVariation.device_type == user["device"].type):
        keyboard.add(cut_variation.name)
    return keyboard


def get_payment_type_to_create() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    keyboard.add(states.PROCEED_BRONOSKIN.back_button)
    for payment_type in PaymentType.select():
        keyboard.add(payment_type.button)
    if config.DISCOUNT_BUTTON:
        keyboard.add(buttons_text.DISCOUNT)
    return keyboard


def get_device_type() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    keyboard.add(states.DEVICE_CREATE.back_button)
    for device_type in DeviceType.select():
        keyboard.add(device_type.name)
    return keyboard


def get_devices_to_create(user_text: str) -> tuple[ReplyKeyboardMarkup, bool]:
    keyboard = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    keyboard.add(buttons_text.CREATE_NEW_DEVICE)
    fuzzy = _fuzzy_device(user_text)
    for device in fuzzy:
        keyboard.add(device)
    result = True if fuzzy else False
    return keyboard, result


def get_brand_to_create(user_text: str) -> tuple[ReplyKeyboardMarkup, bool]:
    keyboard = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    keyboard.add(states.DEVICE_LINE.back_button)
    keyboard.add(buttons_text.CREATE_NEW_BRAND)
    fuzzy = _fuzzy_brand(user_text)
    for brand in fuzzy:
        keyboard.add(brand)
    result = True if fuzzy else False
    return keyboard, result


def proceed_bronoskin(user: User):
    keyboard = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    keyboard.add(states.MATERIAL_VARIATION_LINE.back_button)
    keyboard.add(buttons_text.GET_PAYMENT)
    keyboard.add(buttons_text.GUARANTEE_BRONOSKIN)
    keyboard.add(buttons_text.WRITE_OFF_SKIN)
    keyboard.add(buttons_text.DELAYED_IMPLEMENTATION)

    if "comment" in user:
        keyboard.add(buttons_text.DELETE_COMMENT)
    return keyboard
