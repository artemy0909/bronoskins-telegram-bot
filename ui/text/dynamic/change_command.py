from datetime import datetime

from aiogram.utils.markdown import hbold

from utils.database import EmployeeChange, MaterialType, PaymentType
from utils.manager import User
from utils.misc import MONTH_NAMINGS
from utils.views import get_res_count
from ._samples import material_remnants

BIG_LINE = "________________________"


def change_opened(change: EmployeeChange):
    return f"☀ " + hbold("СМЕНА ОТКРЫТА") + f"\n{BIG_LINE}" \
                                            f"\n👤 {change.worker.short_view()}" \
                                            f"\nОстаток резов: {get_res_count()}"


def change_closed_for_worker(user: User, change: EmployeeChange):
    text = f"🌙 " + hbold("СМЕНА ЗАКРЫТА") + f"\n{BIG_LINE}\n"
    salary = 0
    res_payed = 0
    if change.worker == user.im:
        salary += change.salary
    payments = change.payment_set
    for payment in payments:
        if payment.worker == user.im:
            res_payed += payment.skin.cut_variation.cut_type.res_count
            salary += payment.worker_salary
    mouth_changes = EmployeeChange.select(). \
        where((EmployeeChange.open_datetime.month == datetime.now().month)
              & (EmployeeChange.open_datetime.year == datetime.now().year))
    month_salary = 0
    for change in mouth_changes:
        if change.worker == user.im:
            month_salary += change.salary
        for payment in change.payment_set:
            if payment.worker == user.im:
                month_salary += payment.worker_salary
    text += f" Зарплата за сегодня: {salary} ₽\n Выполнено резов: {res_payed}" \
            f"\n Зарплата за {MONTH_NAMINGS[datetime.now().month]}: {month_salary} ₽"
    return text


def change_closed_for_admins(change: EmployeeChange):
    text = f"🌙 " + hbold("СМЕНА ЗАКРЫТА") + f"\n{BIG_LINE}\n👤 {change.worker.short_view()}\n\n"
    payments = change.payment_set
    refunds = change.refund_set
    write_offs = change.writeoff_set
    delays = change.delayedskin_set
    guarantees = change.guarantee_set
    payed_cuts = 0
    write_off_cuts = 0
    delay_cuts = 0
    guarantee_cuts = 0
    sell_sum = 0
    discount_sum = 0
    extra_sum = 0
    res_production_cost = 0
    material_production_cost = 0
    salary_production_cost = change.salary
    acquiring_commission_cost = 0
    payment_types_sums = {}
    cuts_write_off = 0
    for payment_type in PaymentType.select():
        payment_types_sums[payment_type.name] = 0
    for payment in payments:
        salary_production_cost += payment.worker_salary
        payed_cuts += payment.skin.cut_variation.cut_type.res_count
        cuts_write_off += payment.skin.res_count
        acquiring_commission_cost += payment.money * (payment.commission / 1000)
        sell_sum += payment.base_cost
        if payment.base_cost > payment.money:
            discount_sum += payment.base_cost - payment.money
        else:
            extra_sum += payment.money - payment.base_cost
        res_production_cost += payment.skin.res_cost
        material_production_cost += payment.skin.material_cost
        payment_types_sums[payment.payment_type.name] += payment.money
    refund_sum = 0
    for refund in refunds:
        refund_sum += refund.payment.money
    revenue = sell_sum - discount_sum + extra_sum
    total_cash = revenue - refund_sum
    for write_off in write_offs:
        write_off_cuts += write_off.skin.cut_variation.cut_type.res_count
        cuts_write_off += write_off.skin.res_count
        res_production_cost += write_off.skin.res_cost
        material_production_cost += write_off.skin.material_cost
    for delay in delays:
        delay_cuts += delay.skin.cut_variation.cut_type.res_count
        cuts_write_off += delay.skin.res_count
    for guarantee in guarantees:
        guarantee_cuts += guarantee.new_skin.cut_variation.cut_type.res_count
    cuts_remnants = get_res_count()
    text += hbold("РЕЗЫ") + f"\n Оплаченные: {payed_cuts}\n Утерянные: {write_off_cuts}" \
                            f"\n Отложенные: {delay_cuts}\n Гарантийные: {guarantee_cuts}" \
                            f"\n Резов списано: {cuts_write_off}\n Остаток резов: {cuts_remnants}\n{BIG_LINE}\n"
    res_material_types = {}
    for material_type in MaterialType.select():
        res_material_types[material_type.name] = 0
    for skin in change.bronoskin_set:
        res_material_types[skin.material_variation.first_material.name] += 1
        if skin.material_variation.second_material:
            res_material_types[skin.material_variation.second_material.name] += 1
    text += hbold("РЕЗЫ ПО МАТЕРИАЛУ") + "\n"
    for key, value in res_material_types.items():
        text += f" {key}: {value}\n"
    text += BIG_LINE + "\n"
    text += material_remnants() + BIG_LINE + "\n"
    text += hbold("ВИДЫ ОПЛАТЫ") + "\n"
    for key, value in payment_types_sums.items():
        text += f" {key}: {value} ₽\n"
    text += BIG_LINE + "\n" + hbold("ИТОГИ ОПЕРАЦИЙ") + f"\n Продажи: {sell_sum} ₽\n Возвраты: {refund_sum} ₽" \
                                                        f"\n Скидки: {discount_sum} ₽\n Надбавки: {extra_sum} ₽" \
                                                        f"\n Сменный итог: {total_cash} ₽\n"
    text += BIG_LINE + "\n" + hbold("МАРЖА")
    production_expenses = \
        res_production_cost + material_production_cost + salary_production_cost + round(acquiring_commission_cost)
    gross_profit = revenue - production_expenses
    profitability = round(gross_profit / revenue * 100) if revenue != 0 else 0
    text += f"\n Выручка: {revenue} ₽\n Произв. расходы: {production_expenses} ₽" \
            f"\n   на резы: {res_production_cost} ₽\n   на материал: {material_production_cost} ₽" \
            f"\n   на зарплату: {salary_production_cost} ₽\n   на эквайринг: {round(acquiring_commission_cost)} ₽" \
            f"\n Валовая прибыль: {gross_profit if gross_profit > 0 else 0} ₽\n Рентабельность: {profitability}%"
    return text
