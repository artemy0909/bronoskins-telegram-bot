from aiogram.types import InlineKeyboardMarkup

from ui import inline_commands
from ui.keyboards import buttons_text
from ui.keyboards.inline_keyboards._generators import inline_button
from utils.manager import User


def res_incoming_actions(user: User, res_incoming) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        inline_button(user, buttons_text.DELETE_RES_INCOMING, inline_commands.DELETE_RES_INCOMING,
                      res_incoming_id=res_incoming.id))
    return keyboard
