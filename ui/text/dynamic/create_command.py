from aiogram.utils.markdown import hunderline, hitalic, hcode, hbold

from ui.text.mixins import arg_format
from ui.text.static import SAVE_QUESTION
from utils.manager import User
from utils.misc import ru_mobile_number_mask


def select_material(user: User) -> str:
    return f"{create_bronoskin_args_info(user)}\n💎 Выберите материал реза"


def select_cut_variation(user: User) -> str:
    return f"{create_bronoskin_args_info(user)}\n🏷 Выберите тип реза"


def brand_create_confirm(user: User) -> str:
    return f"• Бренд: {hunderline(user['brand_name'])}\n\n" \
           f"{SAVE_QUESTION}"


def device_create(user: User) -> str:
    return f"• Бренд: {hunderline(user['brand'].name)}\n\n💬 Введите имя нового устройства...\n\n❗ " \
           + hbold("⚠️ Просьба отнестись к вводу наименования устройства ответственно. Если ввести имя устройства с"
                   " орфографической ошибкой или просто не полностью, во-первых, я буду вас ненавидеть, во-вторых,"
                   " поиск этого устройства будет затруднен вашей ошибкой. Спасибо!")


def device_create_confirm(user: User) -> str:
    return f"• Бренд: {hunderline(user['brand'].name)}\n" \
           f"• Имя устройства: {hunderline(user['device_name'])}\n" \
           f"• Тип устройства: {hunderline(user['device_type'].name)}\n\n" \
           f"{SAVE_QUESTION}"


def select_device_type(user: User) -> str:
    return f"• Бренд: {hunderline(user['brand'].name)}\n" \
           f"• Имя устройства: {hunderline(user['device_name'])}\n\n" \
           f"💬 Введите название нового устройства...\n\n"


def select_implementation(user: User) -> str:
    return f"{create_bronoskin_args_info(user)}\n🏷 Выберите реализацию пленки. " \
           + hbold("Отложенная оплата или списание реза требуют комментария.\n\n") \
           + hitalic("ℹ️ Чтобы добавить или изменить комментарий просто напишите ответное сообщение")


def bronoskin_create_confirm(user: User) -> str:
    return hbold("Рез пленки с оплатой") + f"\n{create_bronoskin_args_info(user)}\n" \
                                           f"{SAVE_QUESTION}"


def delayed_payment_create_confirm(user: User) -> str:
    return hbold("Отложенная реализация реза") \
           + f"\n{create_bronoskin_args_info(user)}\n" \
             f"{SAVE_QUESTION}"


def write_off_confirm(user: User) -> str:
    return hbold("Списание реза пленки") \
           + f"\n{create_bronoskin_args_info(user)}\n" \
             f"{SAVE_QUESTION}"


def select_payment_type(user: User) -> str:
    return f"{create_bronoskin_args_info(user)}\n💰 Выберите тип оплаты\n\n" \
           + hitalic("ℹ️ Чтобы изменить стоимость для данной пленки, введите целочисленное значение без"
                     " пробелов и инных символов или процент скидки в формате ") + hcode("XX%")


def type_client_number(user: User) -> str:
    return f"{create_bronoskin_args_info(user)}" \
           f"\n☎️ Введите российский мобильный номер телефона клиента в любом формате"


def select_is_material_ruined(user: User) -> str:
    return f"{create_bronoskin_args_info(user)}\n🗑️ Материал использован или испорчен?"


def create_bronoskin_args_info(user: User) -> str:
    text = ""
    device = user["device"]
    if device:
        text += arg_format("Девайс", user["device"].model_title())
    cut_var = user["cut_variation"]
    if cut_var:
        text += arg_format("Тип реза", cut_var.name)
    material_variation = user["material_variation"]
    if material_variation:
        text += arg_format("Материал пленки", material_variation.name)
    number = user["number"]
    if number:
        text += arg_format("Телефон клиента", ru_mobile_number_mask(number))
    money = user["money"]
    if money:
        text += arg_format("Сумма к оплате", f"{money} ₽")
    payment_type = user["payment_type"]
    if payment_type:
        text += arg_format("Тип оплаты", payment_type.name)
    comment = user["comment"]
    if comment:
        text += arg_format("Комментарий", comment)
    is_material_ruined = user["is_material_ruined"]
    if is_material_ruined:
        text += arg_format("Материал испорчен", "ДА" if is_material_ruined else "НЕТ")
    return text
