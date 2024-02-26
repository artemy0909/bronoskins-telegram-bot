from aiogram.types import ReplyKeyboardMarkup
from ui.keyboards import buttons_text

CONFIRM_KEYBOARD = \
    ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True).row(buttons_text.OK, buttons_text.CANCEL)
