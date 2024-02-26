import json

from aiogram.types import InlineKeyboardButton

from utils.database import CallbackData
from utils.manager import User
from utils.misc import generate_token


def inline_button(user: User, button_text: str, command: str, **kwargs) -> InlineKeyboardButton:
    while True:
        key = generate_token(8)
        if not CallbackData.get_or_none(key=key):
            break
    CallbackData.create(worker=user.im, command=command, key=key, data=json.dumps(kwargs))
    return InlineKeyboardButton(button_text, callback_data=key)
