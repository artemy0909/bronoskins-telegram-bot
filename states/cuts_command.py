from utils.state_machine import StateGroup, State, DEFAULT_STATE

cuts_add_group = StateGroup("cuts add group", on_finish_state=DEFAULT_STATE)
CUTS_COUNT = State("cuts count", cuts_add_group, "количеству резов")
CUTS_PRICE = State("cut price", cuts_add_group)
CUTS_ADD_CONFIRM = State("cut add confirm", cuts_add_group)
