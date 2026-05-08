from telegram import Update
from telegram.ext import Application

from src.container import AppContainer
from src.controllers.telegram_bot.utils.init_handlers import get_handlers, setup_commands
from src.settings.app import app_settings


if __name__ == "__main__":
    container = AppContainer()
    print(app_settings.model_dump_json(indent=4))

    proxy_url = str(app_settings.telegram.proxy)

    application = (
        Application
        .builder()
        .token(app_settings.telegram.token.get_secret_value())
        .proxy(proxy_url)
        .get_updates_proxy(proxy_url)
        .connect_timeout(60)
        .read_timeout(60)
        .write_timeout(60)
        .pool_timeout(60)
        .get_updates_connect_timeout(60)
        .get_updates_read_timeout(180)
        .get_updates_write_timeout(60)
        .get_updates_pool_timeout(60)
        .post_init(setup_commands)
        .build()
    )

    application.add_handlers(get_handlers())
    application.run_polling(
        allowed_updates=Update.ALL_TYPES,
        timeout=180,
        bootstrap_retries=5,
    )