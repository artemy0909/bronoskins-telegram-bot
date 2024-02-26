from aiogram.utils.markdown import hbold, hitalic

from utils.database import MaterialsInventoryIntake


def material_remnants():
    text = hbold("ОСТАТКИ МАТЕРИАЛА\n")
    invent = {}
    for e in MaterialsInventoryIntake.select():
        name = f" {e.material_type.name} ({e.size_x_cm} на {e.size_y_cm})"
        if name not in invent:
            invent[name] = e.worksheet_count
        else:
            invent[name] += e.worksheet_count
        outtakes = e.materialsinventoryouttake_set
        for w in outtakes:
            invent[name] -= w.worksheet_count
    material_exists = False
    for value in invent.values():
        if value:
            material_exists = True
    if material_exists:
        for key, value in invent.items():
            text += f"{key}: {hitalic(str(value) + ' шт.')}\n"
    else:
        text += "Нет материала\n"
    return text
