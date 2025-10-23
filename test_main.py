from telegram import Update
from telegram.ext import Application

from src.container import AppContainer
from src.controllers.telegram_bot.utils.init_handlers import get_handlers, setup_commands
from src.settings.app import app_settings

if __name__ == "__main__":
    container = AppContainer()
    print(app_settings.model_dump_json(indent=4))
    application = (
        Application.builder().token(app_settings.telegram.token.get_secret_value()).post_init(setup_commands).build()
    )

    application.add_handlers(get_handlers())
    application.run_polling(allowed_updates=Update.ALL_TYPES)
