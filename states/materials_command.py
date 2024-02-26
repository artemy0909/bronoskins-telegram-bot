from utils.state_machine import StateGroup, State, DEFAULT_STATE

SELECT_INVENT_ACTION = State("select invent action", button_text="началу")

materials_intake_group = StateGroup("materials inventory line", on_return_state=SELECT_INVENT_ACTION,
                                    on_finish_state=DEFAULT_STATE)
INVENTORIABLE_MATERIAL_TYPE_INTAKE = State("inventoriable material type intake",
                                           materials_intake_group, "выбору материала")
MATERIAL_DIMENSION_TYPE = State("material dimension type", materials_intake_group, "выбору типа поступления")
ROLL_DIMENSION = State("roll dimension", materials_intake_group, "размерности рулона")
SHEET_DIMENSION = State("sheet dimension", materials_intake_group, "размерности листа")
MATERIAL_UNIT_COUNT = State("material unit count", materials_intake_group, "кол-ву единиц поступления")
MATERIAL_INTAKE_COST = State("material unit cost", materials_intake_group)
MATERIAL_INTAKE_CONFIRM = State("material intake confirm", materials_intake_group)

materials_outtake_group = StateGroup("materials outtake line", on_return_state=SELECT_INVENT_ACTION,
                                     on_finish_state=DEFAULT_STATE)
SELECT_INTAKE = State("select intake", materials_outtake_group, "выбору поступления")
MATERIAL_OUTTAKE_COUNT = State("material outtake count", materials_outtake_group)
MATERIAL_OUTTAKE_CONFIRM = State("material outtake confirm", materials_outtake_group)
