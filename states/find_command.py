from utils.state_machine import StateGroup, State, DEFAULT_STATE

films_line = StateGroup("films line", on_finish_state=DEFAULT_STATE)
FILMS_SIGNS = State("film signs", films_line, "выбору признака")
FILMS_SELECTION = State("film selection", films_line, "выбору отбора")
FILMS_OUTPUT_RESULTS_CONFIRM = State("film output results confirm", films_line)

FIND_BY_DATE = State("find by date")
FIND_BY_DEVICE = State("find by device")
FIND_BY_MONEY = State("find by money")
FIND_BY_STUFF = State("find by stuff")
FIND_BY_PAYMENT_TYPE = State("find by payment type")
FIND_BY_CUT_TYPE = State("find by cut var")
FIND_BY_MATERIAL_TYPE = State("find by material type")
