from typing import Final

SKIPP_BUTTON_TEXT: Final[str] = "Пропустить"
FINISH_BUTTON_TEXT: Final[str] = "Завершить"
CANCEL_BUTTON_TEXT: Final[str] = "Отмена"

START_COMMAND_MESSAGE: Final[str] = "Привет!👋\n\n"
MENU_COMMAND_MESSAGE: Final[str] = "Выберите группу продуктов:"
ORDERING_BUTTONS_TEXT: Final[tuple[str, ...]] = ("Доходность по продукту", "Доходность для агента", "Срок продукта")
MENU_CALLBACK_MESSAGE_TEMPLATE: Final[str] = "Выберите сортировку продуктов"
PRODUCT_SELECT_MESSAGE_TEMPLATE: Final[str] = "Выберите продукт"
ADMIN_BUTTONS_TEXT: Final[tuple[str, ...]] = (
    "Добавить группу продуктов",
    "Добавить продукт",
    "Редактировать/удалить группу продуктов",
    "Редактировать/удалить продукт",
)
ADMIN_MESSAGE_TEMPLATE: Final[str] = "Запуск админки. Выберите действие"
ADD_NEW_PRODUCT_TYPE_MESSAGE_TEMPLATE: Final[str] = "Введите название группы продуктов"
ADD_NEW_PRODUCT_MESSAGE_TEMPLATE: Final[str] = "Введите название продукта"
SET_PRODUCT_TYPE_FOR_NEW_PRODUCT_MESSAGE_TEMPLATE: Final[str] = (
    "Выберите группу продуктов, к которой будет относиться новый продукт"
)
ADD_NEW_PRODUCT_PROFITABILITY_MESSAGE_TEMPLATE: Final[str] = (
    "Введите значение «Доходность по продукту» в виде десятичной дроби (пример: 1.25)"
)
ADD_NEW_PRODUCT_AGENT_PROFITABILITY_MESSAGE_TEMPLATE: Final[str] = (
    "Введите значение «Доходность для агента» в виде десятичной дроби (пример: 1.25)"
)
ADD_NEW_PRODUCT_PLACEMENT_PERIOD_MESSAGE_TEMPLATE: Final[str] = (
    "Введите значение «Срок продукта» в целого числа (пример: 5)"
)

ADD_NEW_PRODUCT_DESCRIPTION_MESSAGE_TEMPLATE: Final[str] = (
    f"Введите описание продукта или же вы можете пропустить нажав кнопку «{SKIPP_BUTTON_TEXT}»"
)

ADD_NEW_PRODUCT_FILE_MESSAGE_TEMPLATE: Final[str] = (
    f"Отправьте файл, содержащий описание продукта. Если файла нет, нажмите кнопку {FINISH_BUTTON_TEXT}"
)


PRODUCT_TYPE_SAVED_MESSAGE_TEMPLATE: Final[str] = "Новая группа продуктов «{product_type_name}» успешно добавлена"
PRODUCT_SAVED_MESSAGE_TEMPLATE: Final[str] = (
    "Новый продукт успешно добавлен.\n"
    "Параметры продукта:\n"
    "Название: {name}\n"
    "Доходность по продукту: {profitability}%\n"
    "Доходность для агента: {agent_profitability}%\n"
    "Срок продукта: {placement_period} год/года/лет\n"
    "Группа продуктов: {product_type}\n"
    "Описание: {description}\n"
    "Файл: {file_name}"
)
PRODUCT_INFO_MESSAGE_TEMPLATE: Final[str] = (
    "Параметры продукта:\n"
    "Название: {name}\n"
    "Доходность по продукту: {profitability}%\n"
    "Доходность для агента: {agent_profitability}%\n"
    "Срок продукта: {placement_period} год/года/лет\n"
    "Группа продуктов: {product_type}\n"
)
SELECT_PRODUCT_TYPE_FOR_EDIT_MESSAGE_TEMPLATE: Final[str] = (
    "Выберите группу продуктов, которую хотите отредатктировать/удалить"
)
SELECT_PRODUCT_FOR_EDIT_MESSAGE_TEMPLATE: Final[str] = "Выберите продукт, который хотите отредатктировать/удалить"

SELECT_ACTION_MESSAGE_TEMPLATE: Final[str] = "Выберите действие"
PRODUCT_TYPE_EDIT_ACTIONS_BUTTONS_TEXT: Final[tuple[str, ...]] = (
    "Изменить название группы продуктов",
    "Удалить группу продуктов",
)
PRODUCT_EDIT_ACTIONS_BUTTONS_TEXT: Final[tuple[str, ...]] = (
    "Изменить название продукта",
    "Изменить доходность продукта",
    "Изменить доходность агента",
    "Изменить срок продукта",
    "Изменить описание продукта",
    "Изменить файл-описание продукта",
    "Удалить продукт",
)
ADD_PRODUCT_NEW_NAME_MESSAGE_TEMPLATE: Final[str] = "Введите новое название продукта"
ADD_PRODUCT_NEW_PROFITABILITY_MESSAGE_TEMPLATE: Final[str] = (
    "Введите новое значение «Доходности по продукту» в виде десятичной дроби (пример: 1.25)"
)
ADD_PRODUCT_NEW_AGENT_PROFITABILITY_MESSAGE_TEMPLATE: Final[str] = (
    "Введите новое значение «Доходности для агента» в виде десятичной дроби (пример: 1.25)"
)
ADD_PRODUCT_NEW_PLACEMENT_PERIOD_MESSAGE_TEMPLATE: Final[str] = (
    "Введите новое значение «Срока продукта» в целого числа (пример: 5)"
)
ADD_PRODUCT_NEW_DESCRIPTION_MESSAGE_TEMPLATE: Final[str] = "Введите новое описание продукта"
ADD_PRODUCT_NEW_FILE_MESSAGE_TEMPLATE: Final[str] = "Отправьте новый файл"

DELETE_PRODUCT_TYPE_MESSAGE_TEMPLATE: Final[str] = "Группа продуктов успешно удалена"
DELETE_PRODUCT_MESSAGE_TEMPLATE: Final[str] = "Продукт успешно удален"

EDIT_PRODUCT_TYPE_NAME_MESSAGE_TEMPLATE: Final[str] = "Имя группы продуктов успешно изменено на  «{product_type_name}»"

EDIT_PRODUCT_NAME_MESSAGE_TEMPLATE: Final[str] = "Имя продукта успешно изменено на  «{value}»"
EDIT_PRODUCT_PROFITABILITY_MESSAGE_TEMPLATE: Final[str] = (
    "Новое значение «Доходности по продукту» успешно изменено на {value}"
)
EDIT_PRODUCT_AGENT_PROFITABILITY_MESSAGE_TEMPLATE: Final[str] = (
    "Новое значение «Доходности для агента» успешно изменено на {value}"
)
EDIT_PRODUCT_PLACEMENT_PERIOD_MESSAGE_TEMPLATE: Final[str] = (
    "Новое значение «Срока продукта» успешно изменено на {value}"
)
EDIT_PRODUCT_DESCRIPTION_MESSAGE_TEMPLATE: Final[str] = "Новое описание успешно сохранено"
EDIT_PRODUCT_FILE_MESSAGE_TEMPLATE: Final[str] = "Новый файл успешно сохранен"

SUPPORT_START_MESSAGE_TEMPLATE: Final[str] = (
    f"Начат диалог с поддержкой. Введите свой вопрос.\n\nДля завершения нажмите кнопку «{FINISH_BUTTON_TEXT}»"
)

SUPPORT_DIALOG_QUESTION_TO_SUPPORT_MESSAGE_TEMPLATE: Final[str] = "Вопрос по обращению №{dialog_id}:\n\n {question}"
SUPPORT_DIALOG_ANSWER_TO_USER_MESSAGE_TEMPLATE: Final[str] = "Ответ на ваш вопрос:\n\n {answer}"
SUPPORT_DIALOG_FINISHED_BY_SUPPORT_MESSAGE_TEMPLATE: Final[str] = (
    "Ваш диалог с поддержкой был завершен сотрудником поддержки"
)
SUPPORT_DIALOG_FINISHED_BY_USER_MESSAGE_TEMPLATE: Final[str] = (
    "Ваш диалог по обращению №{dialog_id} был завершен пользователем"
)
SUPPORT_DIALOG_FINISH_MESSAGE_TEMPLATE: Final[str] = "Ваш диалог по обращению №{dialog_id} был завершен"
SUPPORT_DIALOG_FINISHED_MESSAGE_TEMPLATE: Final[str] = "Ваш диалог был успешно завершен"
