from aiogram.types import ReplyKeyboardMarkup

import states.bronoskin_actions as states
from ui.keyboards import buttons_text
from ui.keyboards.reply_keyboards._generators import _linear_generator
from utils.database import CutVariation, PriceList, PaymentType
from utils.manager import User

BACK_TO_ACTION_SELECT = _linear_generator([states.REFUND_BRONOSKIN_COMMENT.back_button])
TYPE_CLIENT_NUMBER = _linear_generator([buttons_text.SKIP])


def select_cut_variation_for_guarantee(user: User):
    keyboard = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    device_type = user["bronoskin"].cut_variation.device_type
    cut_type = user["bronoskin"].cut_variation.cut_type
    res_count = cut_type.res_count
    if res_count == 1:
        for cut_variation in CutVariation.select() \
                .where(CutVariation.device_type == device_type, CutVariation.cut_type == cut_type):
            keyboard.add(cut_variation.name)
    elif res_count == 2:
        for cut_variation in CutVariation.select().where(CutVariation.device_type == device_type):
            keyboard.add(cut_variation.name)
    return keyboard


def select_material(user: User):
    keyboard = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    for price_list_item in PriceList.select().where(PriceList.cut_variation == user["cut_variation"]):
        keyboard.add(price_list_item.material_variation.name)
    return keyboard


def get_payment_type_to_guarantee() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    keyboard.add(states.SELECT_MATERIAL_VARIATION_FOR_GUARANTEE.back_button)
    for payment_type in PaymentType.select():
        keyboard.add(payment_type.button)
    return keyboard
