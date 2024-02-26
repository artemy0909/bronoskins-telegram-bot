import os
from datetime import date

from aiogram.types import InputFile

import config

from loader import bot
from utils import file_generators
from utils.misc import MONTH_NAMINGS
from utils.rights import RIGHTS_BOSS, RIGHTS_ADMIN


async def monthly_report_event(date_: date):
    users_to_send = [i for i in RIGHTS_BOSS.stuff_set] + [i for i in RIGHTS_ADMIN.stuff_set]
    send_to_id = []
    for user in users_to_send:
        logins = [i.telegram_id for i in user.login_set]
        if logins:
            send_to_id.extend(logins)

    file_path = file_generators.monthly_report_xlsx((date_.year, date_.month))
    for id_ in send_to_id:
        await bot.send_document(
            id_, InputFile(file_path, f"Отчет {config.MARKET_NAME} ({MONTH_NAMINGS[date_.month]} {date_.year}).xlsx"),
            caption="Ежемесячный отчет")
    os.remove(file_path)
