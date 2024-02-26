from utils.state_machine import StateGroup, State, DEFAULT_STATE

create_bronoskin_group = StateGroup("create bronoskin main line", on_finish_state=DEFAULT_STATE)
DEVICE_LINE = State("device select", create_bronoskin_group, "выбору устройства")
CUT_VARIATION_LINE = State("cut variation select", create_bronoskin_group, "выбору типа реза")
MATERIAL_VARIATION_LINE = State("material type select", create_bronoskin_group, "выбору материала")
PROCEED_BRONOSKIN = State("proceed bronoskin", create_bronoskin_group, "выбору реализации")
# CLIENT_NUMBER = State("proceed bronoskin", create_bronoskin_group, "вводу номера тел.")
PAYMENT_TYPE_LINE = State("payment type select", create_bronoskin_group)
BRONOSKIN_CONFIRM = State("bronoskin confirm", create_bronoskin_group)

device_create_group = StateGroup("device create", on_finish_state=CUT_VARIATION_LINE, on_return_state=DEVICE_LINE)
BRAND_LINE = State("brand select", device_create_group, "выбору бренда устройства")
DEVICE_CREATE = State("device name input", device_create_group, "вводу названия устройства")
DEVICE_TYPE_LINE = State("device type select", device_create_group, "выбору типа устройства")
DEVICE_CREATE_CONFIRM = State("device create confirm", device_create_group)

brand_create_group = StateGroup("brand create", on_finish_state=DEVICE_CREATE, on_return_state=BRAND_LINE)
BRAND_CREATE = State("brand name input", brand_create_group, "вводу названия бренда")
BRAND_CREATE_CONFIRM = State("brand create confirm", brand_create_group)

write_off_confirm_group = StateGroup(
    "write off confirm", on_finish_state=DEFAULT_STATE, on_return_state=PROCEED_BRONOSKIN)
WRITE_OFF_IS_MATERIAL_RUINED = State("write off is material ruined", write_off_confirm_group)
WRITE_OFF_CONFIRM = State("write off confirm", write_off_confirm_group)

delayed_implementation_confirm_group = StateGroup(
    "delayed implementation confirm", on_finish_state=DEFAULT_STATE, on_return_state=PROCEED_BRONOSKIN)
DELAYED_IMPLEMENTATION_CONFIRM = State("delayed implementation confirm", delayed_implementation_confirm_group)
