from aiogram.utils.markdown import hbold, hitalic

from utils.database import MaterialsInventoryIntake
from utils.manager import User
from utils.misc import BASE_DATE_FORMAT
from ._samples import material_remnants
from ..mixins import line_format, arg_format
from ..static import SAVE_QUESTION


def select_invent_action():
    return f"Выберите действие для продолжения\n\n{material_remnants()}"


def select_dimension_type(user: User):
    return f"{create_material_intake(user)}\nВыберите вид поступления материала"


def type_roll_size(user: User):
    return f"{create_material_intake(user)}\nВведите размерность рулона" \
           f"\n\nℹ️ Формат ввода ширины и длинны рулона в сантиметрах: Ш*Д"


def type_sheet_size(user: User):
    return f"{create_material_intake(user)}\nВведите размерность рабочей области (вырезанный лист)" \
           "\n\nℹ️ Формат ввода ширины и длинны листа в сантиметрах: Ш*Д"


def type_material_unit_count(user: User) -> str:
    if user["roll_size"]:
        return f"{create_material_intake(user)}\nВведите кол-во рулонов на поступление"
    else:
        return f"{create_material_intake(user)}\nВведите кол-во листов на поступление"


def type_intake_cost(user: User):
    return f"{create_material_intake(user)}\nВведите сумму расхода за весь приход материала"


def material_intake_confirm(user: User):
    return f"{create_material_intake(user)}\n" \
           f"{SAVE_QUESTION}"


def create_material_intake(user: User) -> str:
    text = ""
    material_type = user["material_type"]
    if material_type:
        text += arg_format("Тип материала", material_type.name)
    roll_size = user["roll_size"]
    if roll_size:
        text += arg_format("Размер рулона", f"{roll_size[0]}:{roll_size[1]} (см)")
    sheet_size = user["sheet_size"]
    if sheet_size:
        text += arg_format("Размер раб. области", f"{sheet_size[0]}:{sheet_size[1]} (см)")
    worksheet_count_per_roll = user["worksheet_count_per_roll"]
    if worksheet_count_per_roll:
        text += arg_format("Раб. областей в рулоне", worksheet_count_per_roll)
    roll_count = user["roll_count"]
    if roll_count:
        text += arg_format("Кол-во рулонов", roll_count)
    total_worksheet_count = user["total_worksheet_count"]
    if total_worksheet_count:
        text += arg_format("Кол-во раб. областей", total_worksheet_count)
    total_cost = user["total_cost"]
    if total_cost:
        text += arg_format("Общая стоимость", f"{total_cost} ₽")
    worksheet_cost = user["worksheet_cost"]
    if worksheet_cost:
        text += arg_format("Стоимость раб. области", f"{worksheet_cost} ₽")
    return text


def material_incoming_list():
    text = "Выберите номер поступления, чтобы произвести списание:\n\n"
    for e in MaterialsInventoryIntake.select():
        outtakes = e.materialsinventoryouttake_set
        count_outtakes = 0
        for w in outtakes:
            count_outtakes += w.worksheet_count
        if e.worksheet_count - count_outtakes > 0:
            text += f" • " + hbold(f"№{e.id}") + f" {e.material_type.name} ({e.size_x_cm} на {e.size_y_cm})\n" \
                                                 f" └ ({e.datetime.strftime(BASE_DATE_FORMAT)}):" \
                    + hitalic(f" {e.worksheet_count - count_outtakes} шт.\n")
    return text


def material_outtake_confirm(user: User):
    return line_format("Списать из", value=f"Поступление №{user['intake']}",
                       val_uname=MaterialsInventoryIntake.MODEL_CODE, val_id=user['intake'].id, mark="•") \
           + arg_format("Кол-во списания", user["outtake_count"]) \
           + f"\n{SAVE_QUESTION}"
