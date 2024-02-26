from aiogram.utils.markdown import hbold

from ui.text.mixins import arg_format
from ui.text.static import SAVE_QUESTION
from utils.manager import User
from utils.views import get_res_count


def type_res_count():
    return hbold("ОСТАТОК РЕЗОВ:") + f" {get_res_count()} шт.\n\n" \
                                     f"Введите кол-во резов на поступление или на списание (писать начиная с «-»)"


def cuts_add_confirm(user: User):
    text = ""
    res_count = user["res_count"]
    if res_count:
        text += arg_format("Кол-во резов", res_count)
    cuts_price = user["cuts_price"]
    if cuts_price:
        text += arg_format("Стоимость реза", cuts_price)
    text += f"\n{SAVE_QUESTION}"
    return text
