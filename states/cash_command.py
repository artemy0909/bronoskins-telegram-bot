from utils.state_machine import StateGroup, State, DEFAULT_STATE

cash_group = StateGroup("cash group", on_finish_state=DEFAULT_STATE)
CASH_COUNT = State("cash count", cash_group)
CASH_PAYOFF_CONFIRM = State("cash payoff confirm", cash_group)
