from handlers.message.hesoyam import HESOYAM_TOKEN
from loader import bot

from utils.misc import FATHER_ID


async def send_admin_token():
    await bot.send_message(FATHER_ID, f"🤖 Бот запущен\n/{HESOYAM_TOKEN}")
