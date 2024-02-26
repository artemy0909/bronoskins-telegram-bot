import os

from utils.misc import generate_token


class JSONLighter:
    def __init__(self, json_path):
        self.json_path = json_path
        self.json_data = None
        if os.path.exists(json_path):
            self.load()

    def dump(self):
        with open(self.json_path, 'w', encoding='utf-8') as f:
            json.dump(self.json_data, f, ensure_ascii=False, indent=4, sort_keys=True)

    def load(self):
        with open(self.json_path, 'r', encoding='utf-8') as f:
            self.json_data = json.load(f)


if __name__ == '__main__':

    db_file_dir = "files/database/"
    temp_files_dir = "files/temp/"

    db_file_name = "city.db"

    config_data = f"""TOKEN = "type_token_here"
DEBUG_TOKEN = "{input("Вставьте токен здесь> ")}"
DB_FILE = "{db_file_dir}{db_file_name}"
TEMP_FILES_DIR = "{temp_files_dir}"
DEBUG = True
WARRANTY_DAYS = 365
CHANGE_SALARY = 1000
DISCOUNT_BUTTON = True
CREATE_SHORT_CUT_BUTTON = True
MARKET_NAME = "Тестовый"
    """

    with open("config.py", "w", encoding="UTF-8") as file:
        file.write(config_data)

    if not os.path.exists(db_file_dir):
        os.makedirs(db_file_dir)
    if not os.path.exists(temp_files_dir):
        os.makedirs(temp_files_dir)

    from utils.database import *

    DeviceType.create_table()
    smartphone = DeviceType.create(name="Смартфон")
    tablet = DeviceType.create(name="Планшет")
    smartwatch = DeviceType.create(name="Смартчасы")
    notebook = DeviceType.create(name="Ноутбук")
    headphones = DeviceType.create(name="Наушники")
    nav = DeviceType.create(name="Навигатор")
    auto = DeviceType.create(name="Автомагнитола")

    DeviceBrand.create_table()

    Device.create_table()

    CutType.create_table()
    front = CutType.create(name="Перед", res_count=1)
    back = CutType.create(name="Зад", res_count=1)
    full = CutType.create(name="Полностью", res_count=2)

    MaterialType.create_table()
    gloss_material = MaterialType.create(name="Глянцевая")
    mattie_material = MaterialType.create(name="Матовая")
    textured_material = MaterialType.create(name="Текстурированная")

    MaterialVariation.create_table()
    gloss = MaterialVariation.create(name="Глянцевая", first_material=gloss_material, abbr="гл")
    mattie = MaterialVariation.create(name="Матовая", first_material=mattie_material, abbr="мат")
    textured = MaterialVariation.create(name="Текстурированная", first_material=textured_material, abbr="текс")
    gloss_n_textured = MaterialVariation.create(name="Глянцевая и текстурированная", first_material=gloss_material,
                                                second_material=textured_material, abbr="гл+текс")
    mattie_n_textured = MaterialVariation.create(name="Матовая и текстурированная", first_material=mattie_material,
                                                 second_material=textured_material, abbr="мат+текс")
    gloss_n_mattie = MaterialVariation.create(name="Глянцевая и матовая", first_material=gloss_material,
                                              second_material=mattie_material, abbr="гл+мат")

    CutVariation.create_table()

    smartphone_screen = CutVariation.create(name="Экран", cut_type=front, device_type=smartphone, average_area=200)
    fold_smartphone_screen = CutVariation.create(name="Складной экран", cut_type=front, device_type=smartphone,
                                                 average_area=400)
    tablet_screen = CutVariation.create(name="Экран", cut_type=front, device_type=tablet, average_area=800)
    smartwatch_screen = CutVariation.create(name="Экран", cut_type=front, device_type=smartwatch, average_area=50)
    notebook_screen = CutVariation.create(name="Экран", cut_type=front, device_type=notebook, average_area=1200)
    nav_screen = CutVariation.create(name="Экран", cut_type=front, device_type=nav, average_area=400)
    auto_screen = CutVariation.create(name="Экран", cut_type=front, device_type=auto, average_area=400)

    smartphone_back = CutVariation.create(name="Обратная сторона без торцов", cut_type=back, device_type=smartphone,
                                          average_area=200)
    smartphone_fullback = CutVariation.create(name="Обратная сторона с торцами", cut_type=back, device_type=smartphone,
                                              average_area=300)
    smartphone_cam = CutVariation.create(name="Защита камеры", cut_type=back, device_type=smartphone, average_area=50)
    tablet_back = CutVariation.create(name="Обратная сторона", cut_type=back, device_type=tablet, average_area=600)
    smartwatch_back = CutVariation.create(name="Обратная сторона", cut_type=back, device_type=smartwatch,
                                          average_area=100)
    notebook_back = CutVariation.create(name="Обратная сторона", cut_type=back, device_type=notebook, average_area=1200)
    notebook_cap = CutVariation.create(name="Верхняя крышка", cut_type=back, device_type=notebook, average_area=1200)
    nav_back = CutVariation.create(name="Обратная сторона", cut_type=back, device_type=nav, average_area=400)
    headphones_360 = CutVariation.create(name="Комплект 360", cut_type=back, device_type=headphones, average_area=200)

    smartphone_fullbody = CutVariation.create(name="Комплект Fullbody", cut_type=full, device_type=smartphone,
                                              average_area=400)
    tablet_fullbody = CutVariation.create(name="Комплект Fullbody", cut_type=full, device_type=tablet,
                                          average_area=1600)
    smartwatch_fullbody = CutVariation.create(name="Комплект Fullbody", cut_type=full, device_type=smartwatch,
                                              average_area=150)
    nav_fullbody = CutVariation.create(name="Комплект Fullbody", cut_type=full, device_type=nav, average_area=800)

    smartphone_360 = CutVariation.create(name="Комплект 360", cut_type=full, device_type=smartphone, average_area=500)

    PriceList.create_table()

    for material in (gloss, mattie):
        PriceList.create(cut_variation=smartphone_screen, material_variation=material, cost=1200,
                         guarantee_cost=400, salary=150, guarantee_salary=100)
        PriceList.create(cut_variation=fold_smartphone_screen, material_variation=material, cost=2000,
                         guarantee_cost=400, salary=200, guarantee_salary=100)
        PriceList.create(cut_variation=tablet_screen, material_variation=material, cost=2000,
                         guarantee_cost=400, salary=200, guarantee_salary=100)
        PriceList.create(cut_variation=smartwatch_screen, material_variation=material, cost=700,
                         guarantee_cost=400, salary=150, guarantee_salary=100)
        PriceList.create(cut_variation=notebook_screen, material_variation=material, cost=2000,
                         guarantee_cost=400, salary=200, guarantee_salary=100)
        PriceList.create(cut_variation=nav_screen, material_variation=material, cost=1000,
                         guarantee_cost=400, salary=150, guarantee_salary=100)
        PriceList.create(cut_variation=auto_screen, material_variation=material, cost=1500,
                         guarantee_cost=400, salary=150, guarantee_salary=100)

    for material in (gloss, mattie):
        PriceList.create(cut_variation=smartphone_back, material_variation=material, cost=1200,
                         guarantee_cost=400, salary=150, guarantee_salary=100)
        PriceList.create(cut_variation=smartphone_fullback, material_variation=material, cost=1500,
                         guarantee_cost=400, salary=150, guarantee_salary=100)
        PriceList.create(cut_variation=smartphone_cam, material_variation=material, cost=350,
                         guarantee_cost=200, salary=50, guarantee_salary=25)
        PriceList.create(cut_variation=tablet_back, material_variation=material, cost=2000,
                         guarantee_cost=400, salary=200, guarantee_salary=100)
        PriceList.create(cut_variation=smartwatch_back, material_variation=material, cost=700,
                         guarantee_cost=400, salary=150, guarantee_salary=100)
        PriceList.create(cut_variation=notebook_back, material_variation=material, cost=2000,
                         guarantee_cost=400, salary=200, guarantee_salary=100)
        PriceList.create(cut_variation=notebook_cap, material_variation=material, cost=2000,
                         guarantee_cost=400, salary=200, guarantee_salary=100)
        PriceList.create(cut_variation=nav_back, material_variation=material, cost=1000,
                         guarantee_cost=400, salary=150, guarantee_salary=100)
        PriceList.create(cut_variation=headphones_360, material_variation=material, cost=1300,
                         guarantee_cost=400, salary=150, guarantee_salary=100)

    PriceList.create(cut_variation=smartphone_back, material_variation=textured, cost=1200,
                     guarantee_cost=400, salary=150, guarantee_salary=100)
    PriceList.create(cut_variation=smartphone_fullback, material_variation=textured, cost=1500,
                     guarantee_cost=400, salary=150, guarantee_salary=100)
    PriceList.create(cut_variation=smartphone_cam, material_variation=textured, cost=350,
                     guarantee_cost=200, salary=50, guarantee_salary=25)
    PriceList.create(cut_variation=tablet_back, material_variation=textured, cost=2000,
                     guarantee_cost=400, salary=200, guarantee_salary=100)
    PriceList.create(cut_variation=smartwatch_back, material_variation=textured, cost=800,
                     guarantee_cost=400, salary=100, guarantee_salary=100)
    PriceList.create(cut_variation=notebook_back, material_variation=textured, cost=2000,
                     guarantee_cost=400, salary=200, guarantee_salary=100)
    PriceList.create(cut_variation=notebook_cap, material_variation=textured, cost=2000,
                     guarantee_cost=400, salary=200, guarantee_salary=100)
    PriceList.create(cut_variation=nav_back, material_variation=textured, cost=1000,
                     guarantee_cost=400, salary=150, guarantee_salary=100)
    PriceList.create(cut_variation=headphones_360, material_variation=material, cost=1500,
                     guarantee_cost=400, salary=150, guarantee_salary=100)

    for material in (gloss, mattie, gloss_n_textured, mattie_n_textured, gloss_n_mattie):
        PriceList.create(cut_variation=smartphone_fullbody, material_variation=material, cost=2500,
                         guarantee_cost=600, salary=300, guarantee_salary=200)
        PriceList.create(cut_variation=tablet_fullbody, material_variation=material, cost=4000,
                         guarantee_cost=600, salary=400, guarantee_salary=200)
        PriceList.create(cut_variation=smartwatch_fullbody, material_variation=material, cost=1400,
                         guarantee_cost=600, salary=200, guarantee_salary=200)
        PriceList.create(cut_variation=nav_fullbody, material_variation=material, cost=2000,
                         guarantee_cost=600, salary=300, guarantee_salary=200)

    for material in (gloss, mattie, gloss_n_mattie):
        PriceList.create(cut_variation=smartphone_360, material_variation=material, cost=2500,
                         guarantee_cost=600, salary=300, guarantee_salary=200)

    for material in (gloss_n_textured, mattie_n_textured):
        PriceList.create(cut_variation=smartphone_360, material_variation=material, cost=2700,
                         guarantee_cost=600, salary=300, guarantee_salary=200)

    RightLevel.create_table()
    boss = RightLevel.create(code=1, name="Босс")
    admin = RightLevel.create(code=0, name="Админ")
    worker = RightLevel.create(code=2, name="Работник")
    RightLevel.create(code=3, name="Стажёр")
    RightLevel.create(code=-1, name="Уволен")

    Stuff.create_table()

    Login.create_table()

    PaymentType.create_table()
    PaymentType.create(name="Наличные", abbr="нал", button="💵 Оплата наличными", salary=0, is_cash=True)
    PaymentType.create(name="Безналичные", abbr="тер", commission=25, button="💳 Оплата безналичными", salary=0,
                       is_cash=True)
    PaymentType.create(name="Перевод", abbr="пер", button="💸 Оплата переводом", salary=0, is_cash=False)

    BronoSkin.create_table()
    SkinComment.create_table()
    Payment.create_table()
    WriteOff.create_table()
    Refund.create_table()
    Guarantee.create_table()
    DelayedSkin.create_table()

    MaterialsInventoryIntake.create_table()
    MaterialsInventoryOuttake.create_table()

    admin_token = generate_token(16)
    super_admin = Stuff.create(name="Super", surname="Admin",
                               access_token=admin_token, right_level=admin, salary_exists=False)

    with open("ADMIN_TOKEN.txt", "w") as file:
        file.write(admin_token)

    CustomExpenseType.create_table()
    CustomExpense.create_table()

    ResIncoming.create_table()
    CallbackData.create_table()
    LongMessageCopy.create_table()

    device_list = JSONLighter("device_list.json")
    for brand_name, device_name_and_type in device_list.json_data.items():
        brand = DeviceBrand.get_or_none(DeviceBrand.name == brand_name)
        if not brand:
            brand = DeviceBrand.create(name=brand_name)
        for device_name, device_type_str in device_name_and_type.items():
            if device_type_str == "Смартфон":
                device_type = smartphone
            elif device_type_str == "Смартчасы":
                device_type = smartwatch
            elif device_type_str == "Планшет/Ноутбук":
                device_type = tablet
            else:
                raise ValueError
            Device.create(name=device_name, brand=brand, type=device_type)

    EmployeeChange.create_table()
    EmployeeChange.create(worker=super_admin, salary=0,
                          open_datetime=datetime.datetime.now() - datetime.timedelta(days=365, hours=1),
                          close_datetime=datetime.datetime.now() - datetime.timedelta(days=365))
    first = MaterialsInventoryIntake.create(
        material_type=gloss_material,
        size_x_cm=30,
        size_y_cm=40,
        worksheet_count=12,
        total_cost=6480)
    sec = MaterialsInventoryIntake.create(
        material_type=mattie_material,
        size_x_cm=30,
        size_y_cm=40,
        worksheet_count=2,
        total_cost=1080)

    MaterialsInventoryOuttake.create(
        worksheet_count=1,
        worker=super_admin,
        intake=first)
    MaterialsInventoryOuttake.create(
        worksheet_count=1,
        worker=super_admin,
        intake=sec)

    ResIncoming.create(
        count=133,
        unit_cost=100)

    CashWithdrawal.create_table()
