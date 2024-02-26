import xlsxwriter

from utils.database import BronoSkin, Payment, EmployeeChange, Stuff, WriteOff, ResIncoming, \
    MaterialsInventoryIntake, Refund
from utils.misc import generate_token


def film_search_result_html(results: list[BronoSkin]):
    count = len(results)
    text = ""
    i = 1
    for skin in results:
        text += f"<i>{i} из {count}</i>\n\n{skin.full_view()}<hr>"
        i += 1
    file_text = ""
    for line in text.splitlines():
        file_text += line + "<br>"
    file_path = f"files/temp/{generate_token(8)}"
    with open(file_path, "x", encoding="utf-8") as file:
        file.write(file_text)
    return file_path


def message_copy_html(text):
    file_path = f"files/temp/{generate_token(8)}"
    file_text = ""
    for line in text.splitlines():
        file_text += line + "<br>"
    with open(file_path, "x", encoding="utf-8") as file:
        file.write(file_text)
    return file_path


class XLSXEngine:

    def __init__(self, x_start_point=0, y_start_point=0, first_worksheet_name="Лист1"):
        COLOR_BLUE = "#92cddc"
        COLOR_PALE_BLUE = "#b7dee8"
        COLOR_GREEN = "#c4d79b"
        COLOR_PALE_GREEN = "#d8e4bc"
        COLOR_RED = "#ff0000"
        COLOR_PALE_RED = "#fcd5b4"
        COLOR_PURPLE = "#b1a0c7"
        COLOR_PALE_PURPLE = "#ccc0da"
        COLOR_ORANGE = "#ff9900"
        COLOR_PALE_ORANGE = "#ffcc99"
        COLOR_PALE_YELLOW = "#ffff99"

        self.xlsx_path = f"files/temp/{generate_token(8)}"
        self.wb = xlsxwriter.Workbook(self.xlsx_path)
        MONEY_FORMAT = '_- ###0 ₽_-;- ###0 ₽_-;_- "0" ₽_-;_-@_-'
        self.styles = {
            'RES_DETAILED_TITLE': self.add_style(
                bg_color=COLOR_GREEN,
            ),
            'PAID_INFO': self.add_style(
                bg_color=COLOR_PALE_GREEN,
                bold=0,
                align='left'
            ),
            'PAID_MONEY': self.add_style(
                bg_color=COLOR_PALE_GREEN,
                num_format=MONEY_FORMAT,
                bold=0,
                align='left'
            ),
            'GUARANTEE_INFO': self.add_style(
                bg_color=COLOR_PALE_BLUE,
                bold=0,
                align='left'
            ),
            'GUARANTEE_MONEY': self.add_style(
                bg_color=COLOR_PALE_BLUE,
                num_format=MONEY_FORMAT,
                bold=0,
                align='left'
            ),
            'WRITE_OFF_INFO': self.add_style(
                bg_color=COLOR_PALE_ORANGE,
                bold=0,
                align='left'
            ),
            'WRITE_OFF_MONEY': self.add_style(
                bg_color=COLOR_PALE_ORANGE,
                num_format=MONEY_FORMAT,
                bold=0,
                align='left'
            ),
            'DELAYED_SKIN_INFO': self.add_style(
                bg_color=COLOR_PALE_YELLOW,
                bold=0,
                align='left'
            ),
            'DELAYED_SKIN_MONEY': self.add_style(
                bg_color=COLOR_PALE_YELLOW,
                num_format=MONEY_FORMAT,
                bold=0,
                align='left'
            ),
            'ERROR_INFO': self.add_style(
                bg_color=COLOR_RED,
                bold=0,
                align='left'
            ),
            'ERROR_MONEY': self.add_style(
                bg_color=COLOR_RED,
                num_format=MONEY_FORMAT,
                bold=0,
                align='left'
            ),
            'REFUND_TITLE': self.add_style(
                bg_color=COLOR_RED,
            ),
            'REFUND_INFO': self.add_style(
                bg_color=COLOR_PALE_RED,
                bold=0,
                align='left'
            ),
            'REFUND_MONEY': self.add_style(
                bg_color=COLOR_PALE_RED,
                num_format=MONEY_FORMAT,
                bold=0,
                align='left'
            ),
            'GREEN_TITLE': self.add_style(
                font_size=22,
                border=0,
                bottom=1,
                bg_color=COLOR_GREEN,
                align='left'
            ),
            'GREEN_INFO': self.add_style(
                num_format=MONEY_FORMAT,
                border=0,
                bottom=1,
                bold=0,
                bg_color=COLOR_PALE_GREEN,
                align='left'
            ),
            'ORANGE_TITLE': self.add_style(
                font_size=22,
                border=0,
                bottom=1,
                bg_color=COLOR_ORANGE,
                align='left'
            ),
            'ORANGE_INFO': self.add_style(
                num_format=MONEY_FORMAT,
                border=0,
                bottom=1,
                bold=0,
                bg_color=COLOR_PALE_ORANGE,
                align='left'
            ),
            'PURPLE_TITLE': self.add_style(
                font_size=22,
                border=0,
                bottom=1,
                bg_color=COLOR_PURPLE,
                align='left'
            ),
            'PURPLE_INFO': self.add_style(
                num_format=MONEY_FORMAT,
                border=0,
                bottom=1,
                bold=0,
                bg_color=COLOR_PALE_PURPLE,
                align='left'
            ),
            'PURPLE_PERCENT': self.add_style(
                num_format='_- ###0 %_-;- ###0 %_-;_- "0" %_-;_-@_-',
                border=0,
                bottom=1,
                bold=0,
                bg_color=COLOR_PALE_PURPLE,
                align='left'
            ),
            'STUFF_TITLE': self.add_style(
                bg_color=COLOR_BLUE,
            ),
            'STUFF_INFO': self.add_style(
                bg_color=COLOR_PALE_BLUE,
                bold=0,
                align='left'
            ),
            'STUFF_MONEY': self.add_style(
                bg_color=COLOR_PALE_BLUE,
                num_format=MONEY_FORMAT,
                bold=0,
                align='left'
            ),
            'STUFF_PERCENT': self.add_style(
                bg_color=COLOR_PALE_BLUE,
                num_format='_- ###0 %_-;- ###0 %_-;_- "0" %_-;_-@_-',
                bold=0,
                align='left'
            ),
        }
        self.x_reference = x_start_point
        self.y_reference = y_start_point
        self.x_cursor = x_start_point
        self.y_cursor = y_start_point
        self.worksheets = [self.wb.add_worksheet(first_worksheet_name)]
        self.current_worksheet = 0

    def add_worksheet(self, name):
        self.worksheets.append(self.wb.add_worksheet(name))
        self.current_worksheet += 1
        self.x_cursor = self.x_reference
        self.y_cursor = self.y_reference

    @property
    def worksheet(self):
        return self.worksheets[self.current_worksheet]

    def return_cursor(self):
        self.x_cursor = self.x_reference
        self.y_cursor = self.y_reference

    def write(self, text, style_name=None, x_merge=0, y_merge=0):
        if isinstance(text, list):
            for i in text:
                self.write(i, style_name, x_merge, y_merge)
            return
        if x_merge or y_merge:
            if style_name:
                self.worksheet.merge_range(
                    self.y_cursor, self.x_cursor, self.y_cursor + y_merge,
                    self.x_cursor + x_merge, text, self.styles[style_name])
            else:
                self.worksheet.merge_range(
                    self.y_cursor, self.x_cursor, self.y_cursor + y_merge,
                    self.x_cursor + x_merge, text)
            self.x_cursor += x_merge + 1
            self.y_cursor += y_merge
        else:
            if style_name:
                self.worksheet.write(self.y_cursor, self.x_cursor, text, self.styles[style_name])
            else:
                self.worksheet.write(self.y_cursor, self.x_cursor, text)
            self.x_cursor += 1

    def writeln(self, text, style_name=None, x_merge=0, y_merge=0):
        self.write(text, style_name, x_merge, y_merge)
        self.y_cursor += 1 + y_merge
        self.x_cursor = self.x_reference

    @staticmethod
    def num_to_xlsx(x, y):
        def convert_base(num):
            alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            if num < 26:
                return alphabet[num]
            else:
                return convert_base(num // 26) + alphabet[num % 26]

        return f"{convert_base(x)}{y + 1}"

    @staticmethod
    def generate_sum_formula(first_x, first_y, last_x, last_y):
        return f"=SUM({XLSXEngine.num_to_xlsx(first_x, first_y)}:" \
               f"{XLSXEngine.num_to_xlsx(last_x, last_y)})"

    def add_style(self, **style_kwargs):
        style_dict = {
            'border': 1,
            'align': 'center',
            'valign': 'vcenter',
            'bold': 1
        }
        style_dict.update(style_kwargs)
        return self.wb.add_format(style_dict)


def monthly_report_xlsx(month: tuple):
    excel = XLSXEngine(first_worksheet_name="Продажи")
    excel.worksheet.set_column('A:A', 11)
    excel.worksheet.set_column('B:B', 10)
    excel.worksheet.set_column('C:C', 16)
    excel.worksheet.set_column('D:D', 35)
    excel.worksheet.set_column('E:E', 22)
    excel.worksheet.set_column('F:F', 14)
    excel.worksheet.set_column('G:G', 30)
    excel.worksheet.set_column('H:L', 15)
    excel.writeln(
        ["Дата", "ID", "Реализация", "Девайс", "Работник", "Материал", "Тип реза",
         "Рез списано", "Зарплата", "Себестоим.", "По прайсу", "Оплачено"], 'RES_DETAILED_TITLE')
    excel.worksheet.freeze_panes(1, 0)
    count = 0

    revenue = {}
    sells = 0
    discounts = 0
    extra = 0
    acquiring = 0
    res_expenses = 0
    material_expenses = 0

    for skin in BronoSkin.select().where(BronoSkin.datetime.month == month[1], BronoSkin.datetime.year == month[0]):
        date_ = skin.datetime.strftime("%d.%m.%Y")
        guarantee_set = skin.guarantee_set
        payment_set = skin.payment_set
        writeoff_set = skin.writeoff_set
        delayedskin_set = skin.delayedskin_set
        res_expenses += skin.res_cost
        material_expenses += skin.material_cost
        if guarantee_set:
            implementation_ = "Гарантия"
            worker = guarantee_set[0].worker.model_title()
            salary = payment_set[0].worker_salary
            price_cost = payment_set[0].base_cost
            paid = payment_set[0].money
            if paid == 0:
                info_style = 'ERROR_INFO'
                money_style = 'ERROR_MONEY'
            else:
                info_style = 'GUARANTEE_INFO'
                money_style = 'GUARANTEE_MONEY'
        elif payment_set:
            implementation_ = "Оплата"
            worker = payment_set[0].worker.model_title()
            salary = payment_set[0].worker_salary
            price_cost = payment_set[0].base_cost
            paid = payment_set[0].money
            if paid == 0:
                info_style = 'ERROR_INFO'
                money_style = 'ERROR_MONEY'
            else:
                info_style = 'PAID_INFO'
                money_style = 'PAID_MONEY'
        elif writeoff_set:
            implementation_ = "Списание"
            worker = writeoff_set[0].worker.model_title()
            salary = 0
            price_cost = 0
            paid = 0
            info_style = 'WRITE_OFF_INFO'
            money_style = 'WRITE_OFF_MONEY'
        elif delayedskin_set:
            implementation_ = "Отложен"
            worker = delayedskin_set[0].worker.model_title()
            salary = 0
            price_cost = 0
            paid = 0
            info_style = 'DELAYED_SKIN_INFO'
            money_style = 'DELAYED_SKIN_MONEY'
        else:
            implementation_ = "ОШИБКА"
            worker = "ОШИБКА"
            salary = 0
            price_cost = 0
            paid = 0
            info_style = 'ERROR_INFO'
            money_style = 'ERROR_INFO'

        if payment_set:
            payment = payment_set[0]
            payment_type = payment.payment_type
            if payment_type not in revenue:
                revenue[payment_type] = 0
            revenue[payment_type] += payment.money
            sells += payment.base_cost
            acquiring += payment.money * (payment.commission / 1000)
            if payment.money > payment.base_cost:
                extra += payment.money - payment.base_cost
            elif payment.money < payment.base_cost:
                discounts += payment.base_cost - payment.money

        device = skin.device.model_title()
        material = skin.material_variation.abbr
        cut_variation = skin.cut_variation.name
        res_count = skin.res_count
        production_cost = skin.material_cost + skin.res_cost
        excel.write(
            [date_, skin.id, implementation_, device, worker, material, cut_variation, res_count], info_style
        )
        excel.writeln(
            [salary, production_cost, price_cost, paid], money_style
        )
        count += 1
    excel.worksheet.autofilter(0, 0, count, 11)

    excel.add_worksheet("Возвраты")
    excel.writeln(
        ["Дата возврата", "Дата продажи", "ID", "Девайс", "Продал", "Вернул", "Материал",
         "Тип реза", "Произв. расходы", "Сумма возврата"], 'REFUND_TITLE')
    excel.worksheet.freeze_panes(1, 0)

    excel.worksheet.set_column('A:B', 17)
    excel.worksheet.set_column('C:C', 10)
    excel.worksheet.set_column('D:D', 35)
    excel.worksheet.set_column('E:F', 22)
    excel.worksheet.set_column('G:G', 14)
    excel.worksheet.set_column('H:H', 30)
    excel.worksheet.set_column('I:J', 20)

    count = 0

    refunds = 0

    for refund in Refund.select().where(Refund.datetime.month == month[1], Refund.datetime.year == month[0]):
        skin = refund.payment.skin
        date_skin = skin.datetime.strftime("%d.%m.%Y")
        date_refund = refund.datetime.strftime("%d.%m.%Y")
        device = skin.device.model_title()
        seller = refund.payment.worker.model_title()
        refunded = refund.worker.model_title()
        material = skin.material_variation.model_title()
        cut_variation = skin.cut_variation.model_title()
        production_cost = refund.payment.worker_salary + skin.res_cost + skin.material_cost
        refund_money = refund.payment.money
        refunds += refund_money
        excel.write(
            [date_refund, date_skin, refund.id, device, seller, refunded, material,
             cut_variation], 'REFUND_INFO')
        excel.writeln([production_cost, refund_money], 'REFUND_MONEY')
        count += 1
    excel.worksheet.autofilter(0, 0, count, 9)

    excel.add_worksheet("Наличные")
    # todo
    excel.add_worksheet("Материал")
    # todo
    excel.add_worksheet("Резы")
    # todo
    excel.add_worksheet("Работники")
    excel.worksheet.set_column('A:I', 22)
    excel.writeln(
        ["Работник", "ID", "Продано пленок", "Кол-во смен", "Процент брака", "Сумма продаж",
         "Зарплата за смены", "Зарплата за пленки", "Общая зарплата"], 'STUFF_TITLE')
    excel.worksheet.freeze_panes(1, 0)

    salary_expenses = 0

    for stuff in Stuff.select():
        sell_count = 0
        change_count = 0
        write_offs_count = 0
        sell_money = 0
        salary_change = 0
        salary_skins = 0
        for change in EmployeeChange.select().where(
                EmployeeChange.open_datetime.month == month[1], EmployeeChange.open_datetime.year == month[0]):
            worker_payments = change.payment_set.where(Payment.worker == stuff)
            worker_write_offs = change.writeoff_set.where(WriteOff.worker == stuff)
            sell_count += sum([e.skin.cut_variation.cut_type.res_count for e in worker_payments])
            if change.worker == stuff:
                change_count += 1
                salary_change += change.salary
            write_offs_count += sum([e.skin.cut_variation.cut_type.res_count for e in worker_write_offs])
            sell_money += sum([e.money for e in worker_payments])
            salary_skins += sum([e.worker_salary for e in worker_payments])
        if not write_offs_count and not sell_count and not change_count:
            continue
        salary_expenses += salary_change + salary_skins
        worker = stuff.model_title()
        excel.write(
            [worker, stuff.id, sell_count, change_count], 'STUFF_INFO')
        try:
            excel.write(write_offs_count / (sell_count + write_offs_count), 'STUFF_PERCENT')
        except ZeroDivisionError:
            excel.write(0, 'STUFF_PERCENT')

        excel.writeln([sell_money, salary_change, salary_skins, salary_change + salary_skins], 'STUFF_MONEY')

    excel.worksheet.autofilter(0, 0, count, 8)

    excel.x_reference = 1
    excel.y_reference = 1
    excel.add_worksheet("ИТОГИ")
    excel.worksheet.set_column('B:D', 30)

    res_purchase = 0
    for res_incoming in ResIncoming.select().where(
                ResIncoming.datetime.month == month[1], ResIncoming.datetime.year == month[0]):
        res_purchase += res_incoming.count * res_incoming.unit_cost

    material_purchase = 0
    for materials_intake in MaterialsInventoryIntake.select().where(
                MaterialsInventoryIntake.datetime.month == month[1], MaterialsInventoryIntake.datetime.year == month[0]):
        material_purchase += materials_intake.total_cost

    excel.worksheet.set_row(excel.y_cursor, 25, excel.styles['GREEN_TITLE'])
    excel.writeln("Виды оплаты")
    revenue_sum = 0
    for key, value in revenue.items():
        excel.worksheet.set_row(excel.y_cursor, None, excel.styles['GREEN_INFO'])
        excel.writeln([key.name, value])
        revenue_sum += value

    excel.y_cursor += 1
    excel.worksheet.set_row(excel.y_cursor, 25, excel.styles['GREEN_TITLE'])
    excel.writeln("Итоги операций")
    rows = [
        ["Продажи", sells, "(по прайсу)"],
        ["Возвраты", refunds],
        ["Скидки", discounts],
        ["Надбавки", extra],
        ["Итог", excel.generate_sum_formula(2, excel.y_cursor, 2, excel.y_cursor + 3),
         "(продажи - скидки + надбавки - возвраты)"]
    ]
    for row in rows:
        excel.worksheet.set_row(excel.y_cursor, None, excel.styles['GREEN_INFO'])
        excel.writeln(row)

    excel.y_cursor += 1
    excel.worksheet.set_row(excel.y_cursor, 25, excel.styles['ORANGE_TITLE'])
    excel.writeln("Переменные расходы")
    rows = [
        ["Закупка резов", res_purchase],
        ["Закупка материала", material_purchase],
        ["Выплаченная зарплата", 0, "(пока не обращай внимание)"],
        ["Эквайринг", acquiring],
        ["Возврат средств", refunds],
        ["Сумма", excel.generate_sum_formula(2, excel.y_cursor, 2, excel.y_cursor + 4)]
    ]
    for row in rows:
        excel.worksheet.set_row(excel.y_cursor, None, excel.styles['ORANGE_INFO'])
        excel.writeln(row)

    excel.y_cursor += 1
    excel.worksheet.set_row(excel.y_cursor, 25, excel.styles['ORANGE_TITLE'])
    excel.writeln("Производственные расходы")
    rows = [
        ["Затраченные резы", res_expenses],
        ["Затраченный материал", material_expenses],
        ["Зарплата", salary_expenses],
        ["Эквайринг", acquiring],
        ["Сумма", excel.generate_sum_formula(2, excel.y_cursor, 2, excel.y_cursor + 3)]
    ]
    for row in rows:
        excel.worksheet.set_row(excel.y_cursor, None, excel.styles['ORANGE_INFO'])
        excel.writeln(row)

    excel.y_cursor += 1
    excel.worksheet.set_row(excel.y_cursor, 25, excel.styles['PURPLE_TITLE'])
    excel.writeln("Рентабельность")
    rows = [
        ["Выручка", revenue_sum],
        ["Маржинальная прибыль",
         f"={excel.num_to_xlsx(2, excel.y_cursor)}-{excel.num_to_xlsx(2, excel.y_cursor - 10)}"],
        ["Валовая прибыль",
         f"={excel.num_to_xlsx(2, excel.y_cursor)}-{excel.num_to_xlsx(2, excel.y_cursor - 3)}"],
    ]
    for row in rows:
        excel.worksheet.set_row(excel.y_cursor, None, excel.styles['PURPLE_INFO'])
        excel.writeln(row)
    excel.worksheet.set_row(excel.y_cursor, None, excel.styles['PURPLE_PERCENT'])
    excel.writeln(["Маржинальная рентабельность",
                   f"={excel.num_to_xlsx(2, excel.y_cursor - 2)}/{excel.num_to_xlsx(2, excel.y_cursor - 3)}"])
    excel.worksheet.set_row(excel.y_cursor, None, excel.styles['PURPLE_PERCENT'])
    excel.writeln(["Валовая рентабельность",
                   f"={excel.num_to_xlsx(2, excel.y_cursor - 2)}/{excel.num_to_xlsx(2, excel.y_cursor - 4)}"])

    excel.wb.close()
    return excel.xlsx_path
