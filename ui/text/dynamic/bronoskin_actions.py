from aiogram.utils.markdown import hitalic, hcode, hbold

from ui.text.mixins import arg_format
from ui.text.static import SAVE_QUESTION
from utils.manager import User
from utils.misc import ru_mobile_number_mask


def create_guarantee_args_info(user: User) -> str:
    text = ""
    device = user["bronoskin"].device
    if device:
        text += arg_format("Девайс", device.model_title())
    cut_var = user["cut_variation"]
    if cut_var:
        text += arg_format("Тип реза", cut_var.name)
    material_variation = user["material_variation"]
    if material_variation:
        text += arg_format("Материал пленки", material_variation.name)
    money = user["money"]
    if money:
        text += arg_format("Сумма к оплате", f"{money} ₽")
    payment_type = user["payment_type"]
    if payment_type:
        text += arg_format("Тип оплаты", payment_type.name)
    return text


def create_payment_args_info(user: User) -> str:
    text = ""
    device = user["bronoskin"].device
    if device:
        text += arg_format("Девайс", device.model_title())
    cut_var = user["bronoskin"].cut_variation
    if cut_var:
        text += arg_format("Тип реза", cut_var.name)
    material_variation = user["bronoskin"].material_variation
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
    return text


def type_client_number(user: User) -> str:
    return f"{create_payment_args_info(user)}" \
           f"\n☎️ Введите российский мобильный номер телефона клиента в любом формате"


def select_material_type_for_guarantee(user: User) -> str:
    return f"{create_guarantee_args_info(user)}\nВыберите тип материала используемый в гарантии"


def select_cut_variation_for_guarantee(user: User) -> str:
    return f"{create_guarantee_args_info(user)}\nВыберите какой тип реза будет переклеен по гарантии"


def select_payment_type_for_guarantee(user: User) -> str:
    return f"{create_guarantee_args_info(user)}\n💰 Выберите тип оплаты\n\n" \
           + hitalic("ℹ️ Чтобы изменить стоимость для данной пленки, введите целочисленное значение без"
                     " пробелов и инных символов или процент скидки в формате ") + hcode("XX%")


def confirm_guarantee_create(user: User) -> str:
    return f"{create_guarantee_args_info(user)}\n{SAVE_QUESTION}"


def guarantee_create_confirm(user: User) -> str:
    return hbold("Рез пленки с оплатой") + f"\n{create_guarantee_args_info(user)}\n" \
                                           f"{SAVE_QUESTION}"
