from aiogram.types import ReplyKeyboardMarkup

from utils.database import select_all
from utils.misc import fuzzy_sorting


def _linear_generator(text_list: list):
    keyboard = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    for text in text_list:
        keyboard.add(text)
    return keyboard


def _fuzzy_device(user_text: str) -> list:
    devices = select_all("Device")
    brands = select_all("DeviceBrand")
    devices_full_names = fuzzy_sorting(user_text, [f"{brands[device[2] - 1][1]} {device[1]}" for device in devices])
    return devices_full_names


def _fuzzy_brand(user_text: str) -> list:
    brands = select_all("DeviceBrand")
    brand_names = fuzzy_sorting(user_text, [brand[1] for brand in brands])
    return brand_names


def _all_users() -> list:
    return [f"{s[1]} {s[2]}" for s in select_all("Stuff")]
