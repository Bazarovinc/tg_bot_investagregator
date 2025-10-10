from typing import Final

START_COMMAND_NAME: Final[str] = "start"
HELP_COMMAND_NAME: Final[str] = "help"
MENU_COMMAND_NAME: Final[str] = "menu"
ADMIN_COMMAND_NAME: Final[str] = "admin"

START_COMMAND_INFO: Final[str] = "Запуск бота и приветственное сообщение"
HELP_COMMAND_INFO: Final[str] = "Вся информация о командах бота"
MENU_COMMAND_INFO: Final[str] = "Получение группы продуктов"
COMMANDS_INFO: Final[tuple[str, ...]] = (
    f"<b>Доступные команды:</b>\n\n/{START_COMMAND_NAME} - {START_COMMAND_INFO}",
    f"/{HELP_COMMAND_NAME} - {HELP_COMMAND_INFO}/{MENU_COMMAND_NAME} - {MENU_COMMAND_INFO}",
)
