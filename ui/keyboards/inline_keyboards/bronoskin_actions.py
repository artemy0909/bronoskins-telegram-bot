from aiogram.types import InlineKeyboardMarkup

from ui import inline_commands
from ui.keyboards import buttons_text
from ui.keyboards.inline_keyboards._generators import inline_button
from utils.database import Payment, DelayedSkin, EmployeeChange, BronoSkin
from utils.manager import User


def bronoskin_view_actions(user: User, bronoskin) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        inline_button(user, buttons_text.ADD_COMMENT, inline_commands.ADD_COMMENT,
                      bronoskin_id=bronoskin.id))
    keyboard.add(
        inline_button(user, buttons_text.DELETE_BRONOSKIN, inline_commands.DELETE_BRONOSKIN,
                      bronoskin_id=bronoskin.id))

    payment = bronoskin.payment_set
    if payment:
        refund = payment[0].refund_set
        if not refund:
            keyboard.add(
                inline_button(user, buttons_text.REFUND_BRONOSKIN, inline_commands.REFUND_BRONOSKIN,
                              bronoskin_id=bronoskin.id),
                inline_button(user, buttons_text.GUARANTEE_BRONOSKIN, inline_commands.GUARANTEE_BRONOSKIN,
                              bronoskin_id=bronoskin.id))

    delayed_skin = DelayedSkin.get_or_none(skin=bronoskin)
    if delayed_skin:
        keyboard.add(
            inline_button(user, buttons_text.PROCESS_PAYMENT, inline_commands.PROCESS_PAYMENT,
                          bronoskin_id=bronoskin.id))
        keyboard.add(
            inline_button(user, buttons_text.WRITE_OFF_SKIN, inline_commands.WRITE_OFF_SKIN,
                          bronoskin_id=bronoskin.id))

    return keyboard


def change_view_skins(user: User, change: EmployeeChange) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=1)
    i = 1
    for e in change.bronoskin_set:
        if e.guarantee_set:
            text = f"🔵 Рез №{i} гарантия"
        elif e.payment_set:
            payment: Payment = e.payment_set[0]
            if payment.money < payment.base_cost:
                text = f"🟤 Рез №{i} скидка"
            elif payment.money > payment.base_cost:
                text = f"🟣 Рез №{i} наценка"
            else:
                text = f"🟢 Рез №{i} оплачен"
        elif e.delayedskin_set:
            text = f"🟡 Рез №{i} отложенный"
        elif e.writeoff_set:
            text = f"🟠 Рез №{i} списан"
        else:
            raise ValueError
        keyboard.add(inline_button(user, text, inline_commands.GET_SKIN_VIEW, bronoskin_id=e.id))
        i += 1
    i = 1
    for e in change.refund_set:
        skin: BronoSkin = e.payment.skin
        keyboard.add(inline_button(user, f"🔴 Возврат №{i}", inline_commands.GET_SKIN_VIEW, bronoskin_id=skin.id))
        i += 1
    return keyboard
