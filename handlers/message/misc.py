import os

from aiogram import types
from aiogram.types import InputFile

from loader import dp

from ui.text import static

from utils import file_generators
from utils.database import LongMessageCopy
from utils.filters import StateFilter, LinkSwitchFilter
from utils.misc import get_link_id
from utils.state_machine import DEFAULT_STATE


@dp.message_handler(StateFilter(DEFAULT_STATE))
async def process_default_state(message: types.Message):
    await message.reply(
        text=static.USE_COMMANDS)


@dp.message_handler(LinkSwitchFilter(LongMessageCopy.MODEL_CODE))
async def process_long_message_copy_ling(message: types.Message):
    message_copy = LongMessageCopy.get_or_none(id=get_link_id(message.text))
    if message_copy:
        await message.reply(
            text=static.PREPARING_FILE)
        file_path = file_generators.message_copy_html(message_copy.text)
        await message.answer_document(InputFile(file_path, f"Полное сообщение.html"))
        os.remove(file_path)
    else:
        await message.reply(
            text=static.INCORRECT_LINK)
