from aiogram.types import ReplyKeyboardMarkup

import states.materials_command as states
from ui.keyboards import buttons_text
from ui.keyboards.reply_keyboards._generators import _linear_generator
from utils.database import MaterialType, MaterialsInventoryIntake, PaymentType
from utils.manager import User

MATERIAL_DIMENSION_TYPE = _linear_generator([states.INVENTORIABLE_MATERIAL_TYPE_INTAKE.back_button,
                                             buttons_text.ROLL_MATERIAL_TYPE, buttons_text.SHEET_MATERIAL_TYPE])
ROLL_DIMENSION = _linear_generator([states.MATERIAL_DIMENSION_TYPE.back_button])
MATERIAL_UNIT_COUNT = _linear_generator([states.SHEET_DIMENSION.back_button])
MATERIAL_INTAKE_COST = _linear_generator([states.MATERIAL_UNIT_COUNT.back_button])
BACK_TO_SELECT_INTAKE = _linear_generator([states.SELECT_INTAKE.back_button])


def select_invent_action(user: User) -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    keyboard.add(buttons_text.OUTTAKE_MATERIALS)
    if user.is_admin():
        keyboard.add(buttons_text.INTAKE_MATERIALS)
    return keyboard


def get_material_types() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    keyboard.add(states.SELECT_INVENT_ACTION.back_button)
    for material in MaterialType.select():
        keyboard.add(material.name)
    return keyboard


def sheet_dimension(user: User) -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    if user["roll_size"]:
        keyboard.add(states.ROLL_DIMENSION.back_button)
    else:
        keyboard.add(states.MATERIAL_DIMENSION_TYPE.back_button)
    return keyboard


def select_intake_id() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    keyboard.add(states.SELECT_INVENT_ACTION.back_button)
    for e in MaterialsInventoryIntake.select():
        outtakes = e.materialsinventoryouttake_set
        count_outtakes = 0
        for w in outtakes:
            count_outtakes += w.worksheet_count
        if e.worksheet_count - count_outtakes > 0:
            keyboard.add(f"№{e.id}")
    return keyboard

