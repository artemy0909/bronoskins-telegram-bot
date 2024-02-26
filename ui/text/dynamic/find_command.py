from aiogram.utils.markdown import hunderline, hcode, hbold, hitalic

from ui.keyboards import buttons_text
from ui.text.mixins import arg_format
from utils.manager import User


def finder_films_args_info(user: User) -> str:
    if user["films_sign"] == "SKINS_WITH_PAYMENT":
        sign = buttons_text.SKINS_WITH_PAYMENT
    elif user["films_sign"] == "SKINS_WITH_WRITE_OFF":
        sign = buttons_text.SKINS_WITH_WRITE_OFF
    elif user["films_sign"] == "SKINS_WITHOUT_IMPLEMENTATION":
        sign = buttons_text.SKINS_WITHOUT_IMPLEMENTATION
    elif user["films_sign"] == "SKINS_WITH_GUARANTEE":
        sign = buttons_text.SKINS_WITH_GUARANTEE
    elif user["films_sign"] == "SKINS_WITH_REFUND":
        sign = buttons_text.SKINS_WITH_REFUND
    elif user["films_sign"] == "NOT_MATTER":
        sign = buttons_text.NOT_MATTER
    else:
        raise ValueError

    text = f"Выбранный признак пленок: {hunderline(sign)}"

    selection_info = []
    if user["find_by_date_creation"]:
        selection_info.append(arg_format(buttons_text.FIND_BY_DATE_CREATION, user['find_by_date_creation']))
    if user["find_by_date_payment"]:
        selection_info.append(arg_format(buttons_text.FIND_BY_PAYMENT_DATE, user['find_by_date_payment']))
    if user["find_by_date_guarantee"]:
        selection_info.append(arg_format(buttons_text.FIND_BY_GUARANTEE, user['find_by_date_guarantee']))
    if user["find_by_date_refund"]:
        selection_info.append(arg_format(buttons_text.FIND_BY_REFUND_DATE, user['find_by_date_refund']))
    if user["find_by_date_write_off"]:
        selection_info.append(arg_format(buttons_text.FIND_BY_WRITE_OFF_DATE, user['find_by_date_write_off']))
    if user["find_by_payment_type"]:
        selection_info.append(arg_format(buttons_text.FIND_BY_PAYMENT_TYPE, user["find_by_payment_type"].name))
    if user["find_by_cut_type"]:
        selection_info.append(arg_format(buttons_text.FIND_BY_CUT_TYPE, user["find_by_cut_type"].name))
    if user["find_by_material_type"]:
        selection_info.append(arg_format(buttons_text.FIND_BY_MATERIAL_TYPE, user["find_by_material_type"].name))

    if user["find_by_money"]:
        selection_info.append(arg_format(buttons_text.FIND_BY_MONEY_COUNT, f"{user['find_by_money']} ₽"))

    if selection_info:
        text += hbold("\n\nОтборы:\n")
        selection_info.sort()
        text = text + "".join(selection_info)

    return text


def find_results(count: int) -> str:
    return f"{count} результатов найдено. Вывести?\n\n⚠️ Более 10 результатов будут выведены файлом"


def find_by_date_selection(user: User) -> str:
    return f"Введите дату для добавления отбора по дате {user['date_sign_label']}\n\nℹ️ " + \
           hitalic("Вводите дату в формате ") + hcode("ДД.ММ.ГГ") + \
           hitalic(" или диапазон дат в формате ") + hcode("ДД.ММ.ГГ-ДД.ММ.ГГ")


def find_by_stuff_selection(user: User) -> str:
    return f"Выберите пользователя для отбора по {user['stuff_sign_label']}"
