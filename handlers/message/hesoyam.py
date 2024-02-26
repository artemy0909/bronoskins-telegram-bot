import sys

from aiogram import types
from aiogram.types import ReplyKeyboardRemove

from loader import dp
from utils.hesoyam_tokens import *


@dp.message_handler(commands=[HESOYAM_TOKEN])
async def process_admin_command(message: types.Message):
    await message.reply(
        reply_markup=ReplyKeyboardRemove(),
        text=f"/{TERMINATE_PROCESS_TOKEN} - выключить бота\n\n\n\n"
             f"/{SELF_DELETE_TOKEN} - самоуничтожиться")


@dp.message_handler(commands=[TERMINATE_PROCESS_TOKEN])
async def process_admin_command(message: types.Message):
    await message.reply(
        reply_markup=ReplyKeyboardRemove(),
        text="Выключаюсь")
    sys.exit()


@dp.message_handler(commands=[SELF_DELETE_TOKEN])
async def process_self_kill_command(message: types.Message):
    await message.reply(
        text="Ня, пока☠️")
    import os
    import sys
    from utils.database import db
    db.close()
    with open("DESTROY.py", "w", encoding="utf-8") as file:
        file.write("""import os, shutil
thisdir = os.getcwd()
shutil.rmtree(thisdir, ignore_errors=True)
""")
    os.system("python DESTROY.py")
    sys.exit()
