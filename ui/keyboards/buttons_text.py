CREATE_NEW_DEVICE = "✳ Создать новое устройство"
CREATE_NEW_BRAND = "✳ Создать новый бренд"

DISCOUNT = "50%"
SHORT_CUT = "⏩ Шорткат: экран>глянец>оплата"

DELAYED_IMPLEMENTATION = "⏱ Отложенная реализация"
WRITE_OFF_SKIN = "🗑 Списать пленку"
GET_PAYMENT = "💰 Оплата"
DELETE_COMMENT = "❌ Удалить комментарий"
SKIP = "↪️ Пропустить"
OK = "✅ Ок"
CANCEL = "⛔ Отмена"
YES = "ДА"
NO = "НЕТ"

ADD_COMMENT = "💬 Добавить коммент"
DELETE_BRONOSKIN = "❌ Удалить пленку"
REFUND_BRONOSKIN = "😐 Возврат оплаты"
GUARANTEE_BRONOSKIN = "🔄 Произвести гарантию"
PROCESS_PAYMENT = "💰 Произвести оплату"

DELETE_RES_INCOMING = "🗑 Удалить поступление"

SKINS = "Пленки"
DEVICES = "Устройства"
INVENT = "Инвентарь пленок"
TYPES = "Бизнес-логика"
USERS = "Пользователи"

# признаки
SKINS_WITH_PAYMENT = "С оплатой"
SKINS_WITH_WRITE_OFF = "Со списанием"
SKINS_WITHOUT_IMPLEMENTATION = "Без реализации"
SKINS_WITH_GUARANTEE = "C переклейкой по гарантии"
SKINS_WITH_REFUND = "C возвратом"
NOT_MATTER = "Признак не важен"

OUTTAKE_MATERIALS = "Списание"
INTAKE_MATERIALS = "Поступление"

ROLL_MATERIAL_TYPE = "Рулон"
SHEET_MATERIAL_TYPE = "Лист"

# отборы
# общие отборы
FIND_BY_DATE_CREATION = "По дате создания пленки"
FIND_BY_DEVICE = "По названию устройства"
FIND_BY_MATERIAL_TYPE = "По типу материала"
FIND_BY_CUT_TYPE = "По типу реза"
FIND_BY_CREATION_WORKER = "По создателю пленки"
FIND_BY_COMMENT = "По содержанию комментария"

# для отборов пленок с реализацией
FIND_BY_WRITE_OFF_WORKER = "По списавшему пленку"
FIND_BY_PAYMENT_WORKER = "По продавшему пленку"
FIND_BY_REFUND_WORKER = "По вернувшему деньги"
FIND_BY_PAYMENT_DATE = "По дате оплаты пленки"
FIND_BY_WRITE_OFF_DATE = "По дате списания пленки"

FIND_BY_REFUND_DATE = "По дате возврата средств"
FIND_BY_GUARANTEE = "По дате гарантии"

FIND_BY_PAYMENT_TYPE = "По типу оплаты"
FIND_BY_MONEY_COUNT = "По сумме оплаты"

START_SEARCHING = "✅ Начать поиск"

not_matter_sign_button_set = (
    FIND_BY_DATE_CREATION,
    FIND_BY_DEVICE,
    FIND_BY_MATERIAL_TYPE,
    FIND_BY_CUT_TYPE,
    FIND_BY_CREATION_WORKER,
)

payment_sign_button_set = not_matter_sign_button_set + (
    FIND_BY_PAYMENT_WORKER,
    FIND_BY_PAYMENT_DATE,
    FIND_BY_PAYMENT_TYPE,
    FIND_BY_MONEY_COUNT,
)

write_off_sign_button_set = not_matter_sign_button_set + (
    FIND_BY_WRITE_OFF_WORKER,
    FIND_BY_WRITE_OFF_DATE,
)

guarantee_sign_button_set = payment_sign_button_set + (
    FIND_BY_GUARANTEE,
)

refund_sign_button_set = payment_sign_button_set + (
    FIND_BY_REFUND_DATE,
    FIND_BY_REFUND_WORKER,
)
