import datetime
import json

import peewee
from aiogram.utils.markdown import hbold, hitalic, hcode, hunderline
from peewee import *

import config
from utils.misc import BASE_DATETIME_FORMAT, BASE_DATE_FORMAT, ru_mobile_number_mask

db = SqliteDatabase(config.DB_FILE)


def select_all(tab_name) -> list:
    return db.execute_sql(f'SELECT * FROM {tab_name}').fetchall()


def encode_args_str(*args):
    return json.dumps(args)


def decode_args_str(args_json):
    return json.loads(args_json)


RUBBLE_STYLE = "RUBBLE_STYLE"


def check_message_size(func):
    def wrapper(*args, **kwargs):
        text = func(*args, **kwargs)
        if len(text) > 4096:
            copy = LongMessageCopy.create(text=text)
            return f"😔 Из-за ограничений телеграм я не могу отправить сообщение, так как оно слишком длинное. \n" \
                   f"Полное сообщение: /{LongMessageCopy.MODEL_CODE}_{copy.id} "
        else:
            return text

    return wrapper


class BotModel(Model):
    MODEL_NAME = "*MODEL_NAME*"
    MODEL_CODE = "*MODEL_CODE*"
    HOOK_MODELS = ()

    def model_title(self) -> str:
        if "name" in vars(self)["__data__"]:
            return str(self.name)
        return f"{self.MODEL_NAME} №{self._pk}"

    def short_view(self):
        return f"{hunderline(self.model_title())} /{self.MODEL_CODE}_{self._pk}"

    @check_message_size
    def full_view(self, is_admin: bool = False, recursive: int = 0, ref_obj=None):
        MARK = '└'
        text = hbold(self.MODEL_NAME) + f" /{self.MODEL_CODE}_{self._pk}\n"
        data = vars(self)["__data__"]
        for column_meta in self._meta.columns.values():
            item = data[column_meta.name]
            if item is None:
                continue

            if isinstance(column_meta.verbose_name, str):
                line = f"{MARK} {column_meta.verbose_name}: "
            else:
                continue

            if column_meta.help_text:
                format_args = decode_args_str(column_meta.help_text)
                if "rubble" in format_args:
                    if isinstance(column_meta, IntegerField):
                        line += hitalic(f"{item} ₽")
                    else:
                        raise ValueError
                if "for_admins" in format_args and not is_admin:
                    continue
                if "ru_phone" in format_args:
                    if isinstance(column_meta, IntegerField):
                        line += ru_mobile_number_mask(item)
                    else:
                        raise ValueError
                if "percent" in format_args:
                    if isinstance(column_meta, IntegerField):
                        line += hitalic(f"{item / 10} %")
                    else:
                        raise ValueError

            elif isinstance(column_meta, ForeignKeyField):
                obj = column_meta.rel_model.get_by_id(item)
                if obj == ref_obj:
                    continue
                line += obj.short_view()
            elif isinstance(column_meta, CharField):
                line += hitalic(item)
            elif isinstance(column_meta, IntegerField):
                line += hitalic(item)
            elif isinstance(column_meta, FixedCharField):
                line += hcode(item)
            elif isinstance(column_meta, DateTimeField):
                line += hitalic(item.strftime(BASE_DATETIME_FORMAT))
            elif isinstance(column_meta, DateField):
                line += hitalic(item.strftime(BASE_DATE_FORMAT))
            elif isinstance(column_meta, BooleanField):
                if item:
                    line += hunderline("ДА")
                else:
                    line += hunderline("НЕТ")
            else:
                continue

            text += line + "\n"

        if recursive:
            recursive_objects = [[]]

            for i in range(0, recursive):
                if i == 0:
                    for dir_ in dir(self):
                        if "_set" in dir_:
                            attr_ = getattr(self, dir_)
                            if isinstance(attr_, peewee.ModelSelect):
                                for model in attr_:
                                    recursive_objects[0].append(model)
                else:
                    recursive_objects.append([])
                    for model_obj in recursive_objects[i - 1]:
                        for dir_ in dir(model_obj):
                            if "_set" in dir_:
                                attr_ = getattr(model_obj, dir_)
                                if isinstance(attr_, peewee.ModelSelect):
                                    for model in attr_:
                                        recursive_objects[i].append(model)

            if recursive_objects:
                related_objects = [a for b in recursive_objects for a in b]
                text += hbold(f"\nСВЯЗАННЫЕ ЗАПИСИ({len(related_objects)}):\n")
                related_objects.sort(key=lambda x: x.datetime if "datetime" in vars(x)["__data__"] else 0)
                for model in related_objects:
                    text += model.full_view(recursive=0, ref_obj=self)
        return text


class DeviceType(BotModel):
    MODEL_NAME = "Тип девайса"
    MODEL_CODE = "dt"

    name = CharField(unique=True, max_length=32, verbose_name="Тип")

    class Meta:
        database = db


class DeviceBrand(BotModel):
    MODEL_NAME = "Бренд"
    MODEL_CODE = "br"

    name = CharField(unique=True, max_length=64, verbose_name="Имя")

    def model_title(self) -> str: return str(self.name)

    class Meta:
        database = db


class Device(BotModel):
    MODEL_NAME = "Девайс"
    MODEL_CODE = "dv"

    name = CharField(max_length=64, verbose_name="Модель")
    brand = ForeignKeyField(DeviceBrand, verbose_name="Бренд")
    type = ForeignKeyField(DeviceType, verbose_name="Тип")

    def model_title(self) -> str: return f"{self.brand.name} {self.name}"

    class Meta:
        database = db


class CutType(BotModel):
    MODEL_NAME = "Тип реза"
    MODEL_CODE = "ct"

    name = CharField(unique=True, max_length=16, verbose_name="Тип")
    res_count = IntegerField(verbose_name="Кол-во реализуемых резов")

    class Meta:
        database = db


class MaterialType(BotModel):
    MODEL_NAME = "Тип материала"
    MODEL_CODE = "mt"

    name = CharField(unique=True, max_length=64, verbose_name="Тип")

    class Meta:
        database = db


class MaterialVariation(BotModel):
    MODEL_NAME = "Вариант материала"
    MODEL_CODE = "mv"

    name = CharField(unique=True, max_length=64, verbose_name="Имя вариации")
    first_material = ForeignKeyField(MaterialType, verbose_name="Первый материал")
    second_material = ForeignKeyField(MaterialType, null=True, verbose_name="Второй материал")
    abbr = CharField(unique=True, max_length=16, verbose_name="Сокращение")

    class Meta:
        database = db


class RightLevel(BotModel):
    MODEL_NAME = "Уровень прав"
    MODEL_CODE = "rl"

    code = IntegerField(unique=True, verbose_name="Код")
    name = CharField(unique=True, max_length=32, verbose_name="Имя")

    class Meta:
        database = db


class Stuff(BotModel):
    MODEL_NAME = "Пользователь"
    MODEL_CODE = "st"

    name = CharField(max_length=32, verbose_name="Имя")
    surname = CharField(max_length=32, verbose_name="Фамилия")
    access_token = FixedCharField(16, unique=True, verbose_name="Токен доступа",
                                  help_text=encode_args_str("for_admins"))
    right_level = ForeignKeyField(RightLevel, verbose_name="Уровень прав")
    is_salary_exists = BooleanField(default=True, verbose_name="Получает зарплату",
                                    help_text=encode_args_str("for_admins"))
    registration_datetime = DateTimeField(default=datetime.datetime.now, verbose_name="Время регистрации")

    def model_title(self) -> str: return f"{self.name} {self.surname}"

    class Meta:
        database = db


class EmployeeChange(BotModel):
    MODEL_NAME = "Смена"
    MODEL_CODE = "ch"

    salary = IntegerField(default=config.CHANGE_SALARY, help_text=encode_args_str("rubble"))
    open_datetime = DateTimeField(default=datetime.datetime.now)
    close_datetime = DateTimeField(null=True)
    worker = ForeignKeyField(Stuff)

    def model_title(self) -> str: return str(vars(self)["__data__"]["open_datetime"].strftime(BASE_DATE_FORMAT))

    class Meta:
        database = db


class MaterialsInventoryIntake(BotModel):
    MODEL_NAME = "Поступление материала"
    MODEL_CODE = "mi"

    material_type = ForeignKeyField(MaterialType, verbose_name="Материал на поступление")
    size_x_cm = IntegerField(verbose_name="Ширина ед. (см)")
    size_y_cm = IntegerField(verbose_name="Длинна ед. (см)")
    worksheet_count = IntegerField(verbose_name="Кол-во раб областей")
    total_cost = IntegerField(verbose_name="Общая стоимость", help_text=encode_args_str("for_admins", "rubble"))
    datetime = DateTimeField(default=datetime.datetime.now, verbose_name="Время создания")

    class Meta:
        database = db


class MaterialsInventoryOuttake(BotModel):
    MODEL_NAME = "Списание материала"
    MODEL_CODE = "mo"

    worker = ForeignKeyField(Stuff, verbose_name="Создал")
    intake = ForeignKeyField(MaterialsInventoryIntake, verbose_name="Поступление")
    worksheet_count = IntegerField(verbose_name="Кол-во ед. списания")
    datetime = DateTimeField(default=datetime.datetime.now, verbose_name="Время создания")

    class Meta:
        database = db


class CutVariation(BotModel):
    MODEL_NAME = "Вариант реза"
    MODEL_CODE = "cv"

    name = CharField(max_length=64, verbose_name="Имя вариации")
    cut_type = ForeignKeyField(CutType, verbose_name="Тип")
    device_type = ForeignKeyField(DeviceType, verbose_name="Тип подходящих устройств")
    average_area = IntegerField(verbose_name="Ср. размер (мм²)")

    class Meta:
        database = db


class PriceList(BotModel):
    MODEL_NAME = "Прайс"
    MODEL_CODE = "pl"

    cut_variation = ForeignKeyField(CutVariation, verbose_name="Вариант реза")
    material_variation = ForeignKeyField(MaterialVariation, verbose_name="Вариант материала")
    cost = IntegerField(verbose_name="Цена", help_text=encode_args_str("rubble"))
    guarantee_cost = IntegerField(verbose_name="Цена (гарантия)", help_text=encode_args_str("rubble"))
    salary = IntegerField(verbose_name="Зарплата работнику", help_text=encode_args_str("rubble"))
    guarantee_salary = IntegerField(verbose_name="Зарплата работнику (гарантия)", help_text=encode_args_str("rubble"))

    class Meta:
        database = db


class Login(BotModel):
    MODEL_NAME = "Соединение"
    MODEL_CODE = "ln"

    telegram_id = IntegerField(primary_key=True, verbose_name="Телеграм id", help_text=encode_args_str("for_admins"))
    user = ForeignKeyField(Stuff, verbose_name="Пользователь")

    class Meta:
        database = db


class PaymentType(BotModel):
    MODEL_NAME = "Тип оплаты"
    MODEL_CODE = "pt"
    HOOK_MODELS = ("refund", "guarantee")

    name = CharField(unique=True, max_length=32, verbose_name="Имя")
    abbr = CharField(unique=True, max_length=16, verbose_name="Сокращение")
    commission = IntegerField(default=0, verbose_name="Эквайринг", help_text=encode_args_str("percent", "for_admins"))
    button = CharField(unique=True, max_length=16, help_text=encode_args_str("for_admins"))
    salary = IntegerField(verbose_name="Зарплата работнику",
                          help_text=encode_args_str("rubble"))  # todo добавить в нику

    is_cash = IntegerField(verbose_name="Касса", help_text=encode_args_str("for_admins")) # todo добавить в обе базы

    class Meta:
        database = db


class ResIncoming(BotModel):
    MODEL_NAME = "Поступление резов"
    MODEL_CODE = "ri"

    count = IntegerField(verbose_name="Кол-во")
    unit_cost = IntegerField(verbose_name="Стоимость единицы", help_text=encode_args_str("for_admins", "rubble"))
    datetime = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db


class BronoSkin(BotModel):
    MODEL_NAME = "Рез"
    MODEL_CODE = "bs"

    device = ForeignKeyField(Device, verbose_name="Девайс")
    cut_variation = ForeignKeyField(CutVariation, verbose_name="Вариант реза")
    material_variation = ForeignKeyField(MaterialVariation, verbose_name="Вариант материала")
    res_cost = IntegerField(verbose_name="Затраты на рез", help_text=encode_args_str("for_admins", "rubble"))
    res_count = IntegerField(verbose_name="Резов списано")
    material_cost = IntegerField(verbose_name="Затраты на материал (прим.)",
                                 help_text=encode_args_str("for_admins", "rubble"))
    change = ForeignKeyField(EmployeeChange)
    datetime = DateTimeField(default=datetime.datetime.now, verbose_name="Время создания")

    class Meta:
        database = db


class SkinComment(BotModel):
    MODEL_NAME = "Коммент"
    MODEL_CODE = "sc"

    skin = ForeignKeyField(BronoSkin, verbose_name="Пленка")
    worker = ForeignKeyField(Stuff, verbose_name="Создал")
    content = CharField(max_length=1024, verbose_name="Коммент")
    datetime = DateTimeField(default=datetime.datetime.now, verbose_name="Время создания")

    class Meta:
        database = db


class Payment(BotModel):
    MODEL_NAME = "Оплата"
    MODEL_CODE = "pa"

    skin = ForeignKeyField(BronoSkin, unique=True, verbose_name="Пленка")
    money = IntegerField(verbose_name="Сумма оплаты", help_text=encode_args_str("rubble"))
    base_cost = IntegerField(verbose_name="Стоимость по прайсу", help_text=encode_args_str("rubble"))
    payment_type = ForeignKeyField(PaymentType, verbose_name="Тип оплаты")
    commission = IntegerField(default=0, verbose_name="Эквайринг", help_text=encode_args_str("percent", "for_admins"))
    worker = ForeignKeyField(Stuff, verbose_name="Создал")
    client_number = IntegerField(null=True, verbose_name="Тел. клиента", help_text=encode_args_str("ru_phone"))
    worker_salary = IntegerField(verbose_name="Зарплата", help_text=encode_args_str("rubble"))
    change = ForeignKeyField(EmployeeChange)
    warranty_period = DateTimeField(verbose_name="Гарантия до")
    datetime = DateTimeField(default=datetime.datetime.now, verbose_name="Время создания")

    class Meta:
        database = db


class WriteOff(BotModel):
    MODEL_NAME = "Списание реза"
    MODEL_CODE = "wf"

    skin = ForeignKeyField(BronoSkin, verbose_name="Списанный рез")
    worker = ForeignKeyField(Stuff, verbose_name="Создал")
    change = ForeignKeyField(EmployeeChange)
    is_material_ruined = BooleanField(verbose_name="Материал испорчен/использован")
    datetime = DateTimeField(default=datetime.datetime.now, verbose_name="Время создания")

    class Meta:
        database = db


class DelayedSkin(BotModel):
    MODEL_NAME = "Отложенный рез"
    MODEL_CODE = "ds"

    skin = ForeignKeyField(BronoSkin, unique=True, verbose_name="Отложенный рез")
    worker = ForeignKeyField(Stuff, verbose_name="Создал")
    change = ForeignKeyField(EmployeeChange)
    datetime = DateTimeField(default=datetime.datetime.now, verbose_name="Время создания")

    class Meta:
        database = db


class Refund(BotModel):
    MODEL_NAME = "Возврат оплаты"
    MODEL_CODE = "re"

    payment = ForeignKeyField(Payment, unique=True, verbose_name="Возвращена")
    worker = ForeignKeyField(Stuff, verbose_name="Создал")
    change = ForeignKeyField(EmployeeChange)
    datetime = DateTimeField(default=datetime.datetime.now, verbose_name="Время создания")

    class Meta:
        database = db


class Guarantee(BotModel):
    MODEL_NAME = "Гарантия"
    MODEL_CODE = "gu"

    payment = ForeignKeyField(Payment, null=True, verbose_name="Оплата старого реза")
    new_skin = ForeignKeyField(BronoSkin, unique=True, verbose_name="Новый рез")
    worker = ForeignKeyField(Stuff, verbose_name="Создал")
    change = ForeignKeyField(EmployeeChange)
    datetime = DateTimeField(default=datetime.datetime.now, verbose_name="Время создания")

    class Meta:
        database = db


class CustomExpenseType(BotModel):
    name = CharField(unique=True, max_length=64)

    class Meta:
        database = db


class CustomExpense(BotModel):
    expense_type = ForeignKeyField(CustomExpenseType)
    money = IntegerField()
    date = DateField(default=datetime.datetime.today)

    class Meta:
        database = db


class CallbackData(BotModel):
    key = CharField(max_length=8, unique=True, primary_key=True)
    worker = ForeignKeyField(Stuff)
    command = CharField(max_length=32)
    data = CharField(max_length=10240)
    old = BooleanField(default=False)

    class Meta:
        database = db


class LongMessageCopy(BotModel):
    text = CharField(max_length=102400)

    class Meta:
        database = db


class CashWithdrawal(BotModel):  # todo добавить в нику и сити
    MODEL_NAME = "Снятие наличных"
    MODEL_CODE = "cw"

    money = IntegerField(verbose_name="Сумма снятия", help_text=encode_args_str("rubble"))
    worker = ForeignKeyField(Stuff, verbose_name="Снял")
    datetime = DateTimeField(default=datetime.datetime.now, verbose_name="Время создания")

    class Meta:
        database = db


class CurrentChange:
    def __init__(self):
        last_change = EmployeeChange.select().order_by(EmployeeChange.id.desc()).get_or_none()
        if last_change and not last_change.close_datetime:
            self.change = last_change
        else:
            self.change = None

    def open_change(self, worker: Stuff):
        if not worker.is_salary_exists:
            self.change = EmployeeChange.create(worker=worker, salary=0)
        else:
            self.change = EmployeeChange.create(worker=worker)

    def close_change(self):
        if isinstance(self.change, EmployeeChange):
            self.change.close_datetime = datetime.datetime.now()
            self.change.save()
            self.change = None
        else:
            raise ValueError

    def is_opened(self):
        if isinstance(self.change, EmployeeChange):
            return True
        else:
            return False
