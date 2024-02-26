from aiogram.types import ReplyKeyboardMarkup

from utils.database import Payment
from utils.manager import User
from utils.misc import MONTH_NAMINGS


def get_month_year_keyboard(user: User) -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    month_list = {}
    for payment in Payment.select():
        if payment.datetime.year not in month_list:
            month_list[payment.datetime.year] = []
        if payment.datetime.month not in month_list[payment.datetime.year]:
            month_list[payment.datetime.year].append(payment.datetime.month)
    links = {}
    for year, months in month_list.items().__reversed__():
        months.sort(reverse=True)
        for month in months:
            label = f"{MONTH_NAMINGS[month]} {year} г."
            keyboard.add(label)
            links[label] = (year, month)
    user["reports_links"] = links
    return keyboard
