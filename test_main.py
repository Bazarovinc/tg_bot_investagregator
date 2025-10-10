from telegram import Update
from telegram.ext import Application

from src.containers.use_cases import UseCasesContainer
from src.controllers.telegram_bot.utils.init_handlers import get_handlers, setup_commands
from src.settings.app import app_settings

if __name__ == "__main__":
    container = UseCasesContainer()
    application = (
        Application.builder().token(app_settings.telegram.token.get_secret_value()).post_init(setup_commands).build()
    )

    application.add_handlers(get_handlers())
    application.run_polling(allowed_updates=Update.ALL_TYPES)
