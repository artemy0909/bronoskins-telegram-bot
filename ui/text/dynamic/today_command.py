from utils.database import EmployeeChange, Payment
from utils.manager import User
from utils.misc import BASE_DATE_FORMAT
from utils.views import get_res_count


def change_report(user: User, change: EmployeeChange) -> str:
    text = f"{change.open_datetime.strftime(BASE_DATE_FORMAT)}\n\n"
    i = 1
    salary = 0
    if change.worker == user.im:
        salary += change.salary
    payments = change.payment_set
    for payment in payments:
        if payment.worker == user.im:
            salary += payment.worker_salary
    money_count = {}
    for skin in change.bronoskin_set:
        payment = Payment.get_or_none(Payment.skin == skin)
        if not payment:
            continue
        if payment.payment_type not in money_count:
            money_count[payment.payment_type] = 0
        money_count[payment.payment_type] += payment.money
        text += f"/bs_{skin.id}. {skin.device.brand.name} {skin.device.name}" \
                f"   {payment.money}/{payment.payment_type.abbr}   " \
                f"({skin.material_variation.abbr}/{skin.cut_variation.name}/{skin.cut_variation.cut_type.res_count})\n"
        i += 1

    all_money = 0
    if money_count:
        text += "\nКасса: "
        for payment_type, money in money_count.items():
            all_money += money
            text += f"{money}₽/{payment_type.abbr}   "
    text += f"\nСумма: {all_money} ₽"
    text += f"\nЗарплата: {salary} ₽"
    text += f"\nОстаток резов: {get_res_count()}"
    return text
