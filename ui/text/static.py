from aiogram.utils.markdown import hbold

START = "Привет👋\nЧтобы пользоваться этим ботом, нужно ввести токен доступа."
TYPE_DEVICE = "💬 Введите название устройства..."
NEW_CUT = "✂ Создаем новый рез.\n" + TYPE_DEVICE
SELECT_BRAND = "💬 Введите название бренда для нового устройства..."
BRAND_ALREADY_EXISTS = "❌ Бренд с таким названием уже существует, вернитесь обратно, чтобы выбрать его"
DEVICE_ALREADY_EXISTS = "❌ Девайс с таким названием и брендом уже существует, вернитесь обратно, чтобы выбрать его"
DEVICE_NAME_CONTAINS_BRAND = "❌ Имя устройства не может содержать название бренда"
ILLEGAL_SYMBOLS_PASTED = "❌ Введен недопустимый символ или была превышена максимальная длина строки"
NEW_BRAND = "💬 Введите название нового бренда...\n\n❗ " \
            + hbold("⚠️ Просьба отнестись к вводу наименования бренда ответственно. Если ввести название бренда с"
                    " орфографической ошибкой, поиск множества устройств под этим брендом"
                    " будет затруднен. Спасибо!")
SEARCH_IN_PROCESS = "🔎 Поиск..."
PREPARING_FILE = "🧠 Подготовка файла..."
FINDER_TEXT = "🔎 Вот, что я нашел. Для повторной попытки, введите еще раз."
DEVICE_NOT_FOUND = "❌ Не найдено ни одного устройства с похожим названием, попробуйте еще раз или" \
                   " создайте новое устройство."
INCORRECT_OPTION = "❌ Такой опции не существует, используйте одну из доступных кнопок"
INCORRECT_SYMBOLS_USED = "❌ Введен недопустимый символ"
INCORRECT_INPUT = "❌ Введено некорректное значение или использованы недопустимые символы"
INCORRECT_USERNAME = "❌ Такого работника нет"
INCORRECT_COST = "❌ Стоимость не может быть отрицательной"
INCORRECT_LINK = "❌ Ссылка устарела или не существует"
SHORTCUT_INCORRECT = "❌ Шорткат невозможен в данном случае"
COST_CHANGED = "✅ Цена для данной пленки изменена"
COMMENT_REQUIRED = "❌ Требуется комментарий"
COMMENT_ADDED = "✅ Комментарий добавлен"
COMMENT_CHANGED = "✅ Комментарий изменён"
COMMENT_DELETED = "✅ Комментарий удалён"
COMMENT_TOO_LONG = "❌ Комментарий слишком длинный"
ACCESS_DENIED = "❌ У вас нет доступа к этому действию"
SELECT_INVENTORIABLE_MATERIAL = "💎 Выберите материал под списание/приход"
FINDER_CAPTION = "Запись какого типа вы хотите найти в базе данных?\n\n" + hbold("⚠️ Раздел временно работает с "
                                                                                 "ошибками, через пару дней починю")
TYPE_TOKEN_FOR_ACCESS = "🔐 Введите верный токен доступа для доступа к боту"
LOG_IN_SUCCESS = "🔓 Вы успешно вошли в учетную запись"
FILMS_SIGNS = "Выберите признак искомой пленки"
TYPE_MONEY_COUNT = "Введите цифру для добавления отбора по сумме оплаты\n\nℹ️ Сумма должна быть целочисленной"
SELECT_PAYMENT_TYPE = "Выберите тип оплаты для отбора"
SELECT_CUT_TYPE_FOR_FIND = "Выберите тип реза для отбора"
SELECT_MATERIAL_TYPE_FOR_SEARCH = "Выберите тип материала для отбора"
UNDER_DEVELOP = "🛠 В разработке"
NOTHING_FOUNDED = "Не найдено ничего, попробуйте еще раз с другими отборами"
DELETE_BRONOSKIN_CONFIRM = "Удалить запись пленки и все связанные с ней записи?\n\n" + hbold("⚠️ Действие не обратимо")
DELETING_COMPLETED = "🗑 Запись удалена"
SELECT_MONTH = "Выберите месяц, за который хотите получить отчет"
REFUND_BRONOSKIN_CONFIRM = "✳ Выполнить возврат пленки?"
REFUND_BRONOSKIN_COMMENT = "Опишите причину возврата пленки..."
TYPE_BRONOSKIN_COMMENT = "Напишите комментарий..."
CONFIRM_SAVE_COMMENT = "✳ Сохранить комментарий?"
USE_COMMANDS = "😕 Неверный ввод, используйте команды"
BRONOSKIN_NOT_EXIST = "😔 Пленки больше не существует"
BRONOSKIN_ALREADY_REFUNDED = "❌ Уже был произведен возврат"
WARRANTY_WAS_EXPIRED = "❌ Гарантия истекла"
OPEN_CHANGE = "👋 Отправьте фотографию кол-ва резов для открытия смены"
CLOSE_CHANGE = "💤 Чтобы закрыть смену, отправьте фотографию кол-ва резов\n\n" \
               + hbold("⚠️ Перед закрытием смены рекомендуется провести сверку командой /today")
CHANGE_CLOSED = "Смена закрыта"
ONLY_ONE_PHOTO = "👹 Отправьте только ОДНО фото"
CHANGE_OPENED = "Смена открыта, хорошего дня!"
TYPE_CUT_PRICE = "Введите стоимость одного реза"
SELECT_MATERIAL_TYPE_FOR_INTAKE = "Выберите тип материала на поступление"
INCORRECT_WORKSHEET_SIZE = "❌ Неверная размерность, рабочая область меньше размеров рулона"
INTAKE_NOT_FOUND = "❌ Поступление с таким номером и свободным остатком не найдено"
TYPE_OUTTAKE_COUNT = "Введите кол-во раб. областей на списание"
INCORRECT_OUTTAKE_COUNT = "❌ Неверное кол-во списания (больше остатка или равно 0)"
OPEN_CHANGE_REQUIRED = "❌ Необходимо открыть смену. Команда 👉 /change"
SAVE_QUESTION = "✳ Сохранить?"
