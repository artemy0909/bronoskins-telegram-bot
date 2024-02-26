from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import config
from utils.database import CurrentChange
from utils.manager import load_user_dict

bot = Bot(token=config.DEBUG_TOKEN if config.DEBUG else config.TOKEN, parse_mode=types.ParseMode.HTML)

users = load_user_dict()
current_change = CurrentChange()
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
