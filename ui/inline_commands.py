from aiogram.types import CallbackQuery

from loader import users
from utils.database import CallbackData

DELETE_BRONOSKIN = "delete_bronoskin"
REFUND_BRONOSKIN = "refund_bronoskin"
GUARANTEE_BRONOSKIN = "guarantee_bronoskin"
WRITE_OFF_SKIN = "write_off_skin"
ADD_COMMENT = "add_comment"
GET_SKIN_VIEW = "get_skin_view"
DELETE_RES_INCOMING = "delete_res_incoming"
PROCESS_PAYMENT = "process_payment"


def get_callback_command(query: CallbackQuery):
    try:
        user = users[query.from_user.id].im
    except KeyError:
        return
    key = query.data
    callback_data = CallbackData.get_or_none(worker=user, key=key)
    if callback_data and not callback_data.old:
        return callback_data.command
    else:
        return
