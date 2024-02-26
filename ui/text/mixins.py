from datetime import datetime, date

from aiogram.utils.markdown import hunderline, hbold, hitalic

from utils.misc import BASE_DATE_FORMAT, BASE_DATETIME_FORMAT


def title_format(label: str, val_uname: str, val_id: int):
    return f"{hbold(label)} /{val_uname}_{str(val_id)}\n"


def line_format(label: str, value, val_uname: str = None, val_id: int = None, mark: str = '└'):
    if bool(val_uname) != bool(val_id):
        raise ValueError
    if isinstance(value, datetime):
        value = value.strftime(BASE_DATETIME_FORMAT)
    if isinstance(value, date):
        value = value.strftime(BASE_DATE_FORMAT)
    if isinstance(value, list) and len(value) == 2 and isinstance(value[0], date) and isinstance(value[1], date):
        value = f"c {value[0].strftime(BASE_DATE_FORMAT)} по {value[1].strftime(BASE_DATE_FORMAT)}"
    link = f" /{val_uname}_{str(val_id)}" if val_uname and val_id else ""
    return f"{mark} {label}: {hunderline(value) if val_uname and val_id else hitalic(value)}{link}\n"


def arg_format(label: str, value):
    return line_format(label, value, mark="•")
