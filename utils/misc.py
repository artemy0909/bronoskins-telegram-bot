import typing
from datetime import datetime
from random import choice
from string import ascii_letters, digits

from fuzzywuzzy.fuzz import partial_ratio, ratio, WRatio, token_set_ratio

FATHER_ID = 751541260
REGEXP_FOR_DEVICE_NAMES = r'^[A-Za-zА-Яа-я0-9 _\-,.\/|\\()":;+=*&!#~?№\[\]{}<>\'@%]{2,64}$'
REGEXP_FOR_STUFF_NAMES = r'^[А-Яа-я ]{2,64}$'
REGEXP_FOR_RU_MOBILE_NUMBERS = r'^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$'
REGEXP_FOR_SIZE = r"^[\d]+\*[\d]+$"
MONTH_NAMINGS = ("None", 'январь', 'февраль', 'март', 'апрель', 'май', 'июнь',
                 'июль', 'август', 'сентябрь', 'октябрь', 'ноябрь', 'декабрь')
MONTH_NAMINGS_GEN = ("None", 'января', 'февраля', 'марта', 'апреля', 'мая', 'июня',
                     'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря')
BASE_DATE_FORMAT = '%d.%m.%Y'
BASE_DATETIME_FORMAT = BASE_DATE_FORMAT + ' %H:%M:%S'


def generate_token(length: int):
    return ''.join(choice(ascii_letters + digits) for _ in range(length))


def benchmark(func):
    from datetime import datetime

    def wrapper(*args, **kwargs):
        t = datetime.now()
        res = func(*args, **kwargs)
        print(func.__name__, datetime.now() - t)
        return res

    return wrapper


def fuzzy_sorting(query_str: str, str_list: typing.List[str], threshold_score: int = 40, max_result_len: int = 250,
                  scorers: typing.List[callable] = None) -> typing.List[str]:
    if scorers is None:
        scorers = [ratio, WRatio, partial_ratio, token_set_ratio]
    result = []
    for str_item in str_list:
        score = sum([scorer(query_str, str_item) for scorer in scorers]) / len(scorers)
        if score > threshold_score:
            result.append((score, str_item))
    result.sort(reverse=True)
    if len(result) > max_result_len:
        result = result[:max_result_len]
    return [i[1] for i in result]


def try_str_to_date_range(text: str):
    dates = text.split('-')
    if len(dates) == 2:
        first_date = convert_str_to_date(dates[0])
        last_date = convert_str_to_date(dates[1])
        if first_date == last_date:
            return first_date
        if first_date and last_date:
            return [first_date, last_date] if first_date < last_date else [last_date, first_date]
        else:
            return
    elif len(dates) == 1:
        return convert_str_to_date(dates[0])
    else:
        return


def convert_str_to_date(date_string):
    return datetime.strptime(date_string, "%d.%m.%y").date()


def convert_to_int(text: str):
    try:
        return int(text)
    except ValueError:
        return


def get_link_id(text: str):
    try:
        return int(text[4:])
    except ValueError:
        return


def ru_mobile_number_convert(text: str):
    if len(text) < 10:
        return
    VALID_CHARS = "-_() "
    result = ""
    if text[0] == "8":
        text = text[1:]
    elif text[0:2] == "+7":
        text = text[2:]
    for e in text:
        if e in VALID_CHARS:
            continue
        elif e.isdecimal():
            result += e
        else:
            return
    if len(result) == 10 and result[0] == "9":
        return int(result)
    return


def ru_mobile_number_mask(number: int):
    str_num = str(number)
    if len(str_num) != 10:
        raise ValueError
    return f"+7-{str_num[0:3]}-{str_num[3:6]}-{str_num[6:8]}-{str_num[8:10]}"


def calculate_worksheet_count(roll_size_x: int, roll_size_y: int, sheet_size_x: int, sheet_size_y: int) -> int:
    return max((roll_size_x // sheet_size_x) * (roll_size_y // sheet_size_y),
               (roll_size_x // sheet_size_y) * (roll_size_y // sheet_size_x))
