from datetime import date, timedelta

from utils.database import Device, select_all, DeviceBrand, DeviceType, CutType, \
    CutVariation, PriceList, PaymentType, Payment, BronoSkin, WriteOff, Guarantee, Refund, Stuff, ResIncoming, \
    MaterialsInventoryOuttake, MaterialVariation, MaterialType, MaterialsInventoryIntake, CashWithdrawal, EmployeeChange
from utils.manager import User


def get_device_by_full_name(user_text: str) -> Device:
    devices = select_all("Device")
    brands = select_all("DeviceBrand")
    devices_list = [(f"{brands[device[2] - 1][1]} {device[1]}", device[0]) for device in devices]
    for device_name, device_id in devices_list:
        if user_text == device_name:
            return Device.get_by_id(device_id)


def get_stuff_by_full_name(user_text: str) -> Device:
    stuff = [(f"{s[1]} {s[2]}", s[0]) for s in select_all("Stuff")]
    for user_name, user_id in stuff:
        if user_text == user_name:
            return Stuff.get_by_id(user_id)


def get_brand_by_name(user_text: str) -> DeviceBrand:
    return DeviceBrand.get_or_none(name=user_text)


def get_material_variation_by_name(user_text: str) -> MaterialVariation:
    return MaterialVariation.get_or_none(name=user_text)


def get_device_type_by_name(user_text: str) -> DeviceType:
    return DeviceType.get_or_none(name=user_text)


def get_cut_var_by_name_n_device_type(user_text: str, device_type: DeviceType) -> CutVariation:
    return CutVariation.get_or_none((CutVariation.name == user_text)
                                    & (CutVariation.device_type == device_type))


def get_cut_type_by_name(user_text: str) -> CutType:
    return CutType.get_or_none(name=user_text)


def get_skin_price(user: User, guarantee=False) -> int:
    price = PriceList.get((PriceList.cut_variation == user["cut_variation"])
                          & (PriceList.material_variation == user["material_variation"]))
    if not guarantee:
        return price.cost
    else:
        return price.guarantee_cost


def get_material_type_by_name(user_text: str) -> MaterialType:
    return MaterialType.get_or_none(name=user_text)


def get_payment_type(user_text: str) -> PaymentType:
    return PaymentType.get_or_none(button=user_text)


def check_brand_exist(input_brand_name: str) -> bool:
    return input_brand_name.lower() in [brand.name.lower() for brand in DeviceBrand.select()]


def check_device_exist(brand, input_device_name) -> bool:
    return input_device_name.lower() in [device.name.lower() for device in Device.select().where(Device.brand == brand)]


def get_payments_by_date(date_: date) -> list[Payment]:
    result = []
    for payment in Payment.select():
        if payment.datetime.date() == date_:
            result.append(payment)
    return result


def find_films(user: User) -> list[BronoSkin]:
    def search_by_date(date_case, list_of_objects):
        result = []
        date_range = []
        if isinstance(date_case, list) and len(date_case) == 2:
            delta = date_case[1] - date_case[0]
            for i in range(delta.days + 1):
                date_range.append(date_case[0] + timedelta(i))
        else:
            date_range = [date_case]
        for object_ in list_of_objects:
            if object_.datetime.date() in date_range:
                result.append(object_)
        return result

    def search_by_stuff(worker, list_of_objects):
        result = []
        for object_ in list_of_objects:
            if object_.worker == worker:
                result.append(object_)
        return result

    if user["films_sign"] == "SKINS_WITH_PAYMENT":
        payments = [i for i in Payment.select()]
        skins = [i.skin for i in payments]
    elif user["films_sign"] == "SKINS_WITH_WRITE_OFF":
        write_offs = [i for i in WriteOff.select()]
        skins = [i.skin for i in write_offs]
    elif user["films_sign"] == "SKINS_WITHOUT_IMPLEMENTATION":
        all_skins = [i for i in BronoSkin.select()]
        payments = [i for i in Payment.select()]
        # guarantees = [i for i in Guarantee.select()]
        write_offs = [i for i in WriteOff.select()]
        filtered_skins = []
        for skin in all_skins:
            implementation_exist = False
            for payment in payments:
                if skin == payment.skin:
                    implementation_exist = True
                    break
            if implementation_exist:
                continue
            for write_off in write_offs:
                if skin == write_off.skin:
                    implementation_exist = True
                    break
            if implementation_exist:
                continue
            if implementation_exist:
                continue
            filtered_skins.append(skin)
        skins = filtered_skins
    elif user["films_sign"] == "SKINS_WITH_GUARANTEE":
        guarantees = [i for i in Guarantee.select()]
        skins = [i.payment.skin for i in guarantees]
    elif user["films_sign"] == "SKINS_WITH_REFUND":
        refunds = [i for i in Refund.select()]
        skins = [i.payment.skin for i in refunds]
    elif user["films_sign"] == "NOT_MATTER":
        skins = BronoSkin.select()
    else:
        raise ValueError

    if user["find_by_date_creation"]:
        skins = search_by_date(user["find_by_date_creation"], skins)
    if user["find_by_date_payment"]:
        payments = search_by_date(
            user["find_by_date_payment"], [Payment.get(Payment.skin == skin) for skin in skins])
        skins = [i.skin for i in payments]
    if user["find_by_date_refund"]:
        refunds = search_by_date(
            user["find_by_date_refund"], [Refund.get(Refund.payment.skin == skin) for skin in skins])
        skins = [i.payment.skin for i in refunds]
    if user["find_by_date_write_off"]:
        write_offs = search_by_date(
            user["find_by_date_refund"], [WriteOff.get(WriteOff.skin == skin) for skin in skins])
        skins = [i.skin for i in write_offs]

    if user["find_by_device"]:
        result_ = []
        for skin in skins:
            if skin.device == user["find_by_device"]:
                result_.append(skin)
        skins = result_

    if user["find_by_creation_worker"]:
        skins = search_by_stuff(user["find_by_creation_worker"], skins)
    if user["find_by_write_off_worker"]:
        write_offs = search_by_stuff(
            user["find_by_write_off_worker"], [WriteOff.get(WriteOff.skin == skin) for skin in skins])
        skins = [i.skin for i in write_offs]
    if user["find_by_payment_worker"]:
        payments = search_by_stuff(
            user["find_by_payment_worker"], [Payment.get(Payment.skin == skin) for skin in skins])
        skins = [i.skin for i in payments]
    if user["find_by_refund_worker"]:
        refunds = search_by_stuff(
            user["find_by_refund_worker"], [Refund.get(Refund.payment.skin == skin) for skin in skins])
        skins = [i.payment.skin for i in refunds]

    if user["find_by_payment_type"]:
        result_ = []
        for payment in [Payment.get(Payment.skin == skin) for skin in skins]:
            if payment.payment_type == user["find_by_payment_type"]:
                result_.append(payment)
        skins = [i.skin for i in result_]
    if user["find_by_cut_type"]:
        result_ = []
        for skin in skins:
            if skin.cut_variation.cut_type == user["find_by_cut_type"]:
                result_.append(skin)
        skins = result_

    if user["find_by_money"]:
        result_ = []
        for payment in [Payment.get(Payment.skin == skin) for skin in skins]:
            if payment.money == user["find_by_money"]:
                result_.append(payment)
        skins = [i.skin for i in result_]

    return skins


def get_res_count():
    count = 0
    for res_incoming in ResIncoming.select():
        count += res_incoming.count
    for skin in BronoSkin.select():
        count -= skin.res_count
    return count


def get_material_production_cost(user: User):
    material_production_cost = 0
    for material in (user["material_variation"].first_material, user["material_variation"].second_material):
        if material:
            if material == MaterialType.get(name="Текстурированная"):  # todo временное решение!
                cost_per_worksheet = 600
                worksheet_area = 1200
                device_area = user["cut_variation"].average_area
                material_production_cost += round(cost_per_worksheet * (device_area / worksheet_area))
            else:
                last_material_write_off = None
                for e in MaterialsInventoryOuttake.select().order_by(
                        MaterialsInventoryOuttake.datetime.desc()):
                    if e.intake.material_type == material:
                        last_material_write_off = e
                intake = last_material_write_off.intake
                cost_per_worksheet = intake.total_cost / intake.worksheet_count
                worksheet_area = intake.size_x_cm * intake.size_y_cm
                device_area = user["cut_variation"].average_area
                material_production_cost += round(cost_per_worksheet * (device_area / worksheet_area))

    return material_production_cost


def get_res_production_cost(user: User):
    res_production_cost = 0
    count_used = 1
    for skin in BronoSkin.select():
        count_used += skin.res_count
    for res_incoming in ResIncoming.select():
        res_cost = res_incoming.unit_cost
        count_used -= res_incoming.count
        if count_used <= 0:
            res_production_cost = res_cost * user["cut_variation"].cut_type.res_count
            break
    if not res_production_cost:
        res_production_cost = ResIncoming.select(). \
                                  order_by(ResIncoming.id.desc()).get().unit_cost * user[
                                  "cut_variation"].cut_type.res_count
    return res_production_cost


def get_worker_salary(user, guarantee=False) -> int:
    if not user.im.is_salary_exists:
        return 0
    price = PriceList.get(cut_variation=user["cut_variation"], material_variation=user["material_variation"])
    if not guarantee:
        return price.salary + user["payment_type"].salary * user["cut_variation"].cut_type.res_count
    else:
        return price.guarantee_salary


def get_intake_by_id(id_: int) -> MaterialsInventoryIntake:
    return MaterialsInventoryIntake.get_or_none(id=id_)


def check_intake_remains(intake) -> int:
    count = intake.worksheet_count
    for w in intake.materialsinventoryouttake_set:
        count += w.worksheet_count
    return count


def get_current_cash_count() -> int:
    cash_type = PaymentType.get_or_none(is_cash=True)
    if cash_type:
        cash_payments = cash_type.payment_set
        if not cash_payments:
            return 0
    else:
        return 0

    cash_sum = 0
    for p in cash_payments:
        cash_sum += p.money

    return cash_sum


def get_my_salary_revenue(user: User) -> int:
    changes = EmployeeChange.select().where(EmployeeChange.worker == user.im)
    payments = Payment.select().where(Payment.worker == user.im)
    payoffs = CashWithdrawal.select().where(CashWithdrawal.worker == user.im)
    return sum([p.worker_salary for p in payments]) + sum([c.salary for c in changes]) - sum([p.money for p in payoffs])
