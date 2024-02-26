from aiogram.utils.markdown import hitalic

from ui.text.static import SAVE_QUESTION
from utils.manager import User
from utils.views import get_current_cash_count, get_my_salary_revenue


def write_num_to_withdrawal(user: User) -> str:
    return ((f"💵 Текущее кол-во наличных в кассе: {get_current_cash_count()} ₽\n"
            f"Остаток вашей зарплаты: {get_my_salary_revenue(user)} ₽\n\n") +
            hitalic("ℹ️ Чтобы снять сумму из кассы введите значение, которое вам необходимо снять"))


def confirm_withdrawal(user: User):
    money = user['money_count']
    return (f"• Сумма на списание: {money} ₽\n"
            f"• Остаток зарплаты после списания: {get_my_salary_revenue(user) - money} ₽\n"
            f"• Остаток наличных в кассе после списания: {get_current_cash_count() - money} ₽\n\n"
            f"{SAVE_QUESTION}")

