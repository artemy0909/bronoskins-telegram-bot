from utils.state_machine import State, StateGroup, DEFAULT_STATE

VIEW_BRONOSKIN = State("view bronoskin")
DELETE_BRONOSKIN_CONFIRM = State("material count input")
CHANGE_DATETIME_BRONOSKIN = State("change datetime bronoskin")
COPY_BRONOSKIN_CONFIRM = State("copy bronoskin confirm")
refund_bronoskin_group = StateGroup("refund bronoskin group", on_finish_state=DEFAULT_STATE)
REFUND_BRONOSKIN_COMMENT = State("refund bronoskin comment", refund_bronoskin_group, "выбору действия")
REFUND_BRONOSKIN_CONFIRM = State("refund bronoskin confirm", refund_bronoskin_group)

new_comment_bronoskin_group = StateGroup("new comment bronoskin group", on_finish_state=DEFAULT_STATE)
BRONOSKIN_COMMENT = State("comment bronoskin", new_comment_bronoskin_group, "выбору действия")
NEW_COMMENT_BRONOSKIN_CONFIRM = State("new comment bronoskin confirm", new_comment_bronoskin_group)

create_guarantee_group = StateGroup("create guarantee group", on_finish_state=DEFAULT_STATE)
SELECT_CUT_VARIATION_FOR_GUARANTEE = State("select cut type for guarantee", create_guarantee_group, "выбору типа реза")
SELECT_MATERIAL_VARIATION_FOR_GUARANTEE = State("select material variation for guarantee", create_guarantee_group)
SELECT_PAYMENT_TYPE_FOR_GUARANTEE = State("select payment type for guarantee", create_guarantee_group)
GUARANTEE_CREATE_CONFIRM = State("guarantee create confirm", create_guarantee_group)

delayed_skin_payment = StateGroup("delayed skin payment", on_finish_state=DEFAULT_STATE)
TYPE_CLIENT_NUMBER = State("type client number", delayed_skin_payment, "вводу номера тел.")
SELECT_PAYMENT_TYPE_FOR_DELAYED = State("select payment type for delayed", delayed_skin_payment)
PAYMENT_CONFIRM = State("payment confirm", delayed_skin_payment)
