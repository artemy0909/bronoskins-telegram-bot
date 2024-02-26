from aiogram import types
from aiogram.types import ReplyKeyboardRemove

from loader import dp, users
from ui.text import static
from utils.database import Login, Stuff
from utils.filters import OnExitFilter, UserNotAuthFilter
from utils.manager import User


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply(
        reply_markup=ReplyKeyboardRemove(),
        text=static.START)


@dp.message_handler(UserNotAuthFilter())
async def process_login_input(message: types.Message):
    tried = Stuff.get_or_none(Stuff.access_token == message.text)
    if tried:
        users[message.from_user.id] = User(tried)
        Login.create(telegram_id=message.from_user.id, user=tried.id)
        await message.reply(
            text=static.LOG_IN_SUCCESS)
    else:
        await message.reply(
            text=static.TYPE_TOKEN_FOR_ACCESS)


@dp.my_chat_member_handler(OnExitFilter())
async def process_stop_bot(chat_member: types.ChatMemberUpdated):
    if chat_member.from_user.id in users:
        Login.get_by_id(chat_member.from_user.id).delete_instance()
        del users[chat_member.from_user.id]
