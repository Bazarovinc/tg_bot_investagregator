import uvicorn
from fastapi import FastAPI, Request, Response
from loguru import logger
from telegram import Update
from telegram.ext import Application

from src.container import AppContainer
from src.controllers.telegram_bot.utils import get_handlers
from src.controllers.telegram_bot.utils.init_handlers import setup_commands
from src.settings.app import app_settings

# Инициализация FastAPI приложения
app = FastAPI()


application = Application.builder().token(app_settings.telegram.token.get_secret_value()).build()
application.add_handlers(get_handlers())


# Вебхук для обработки входящих обновлений от Telegram
@app.post("/webhook")
async def webhook(request: Request) -> Response:
    data = await request.json()
    logger.info(data)
    update = Update.de_json(data, application.bot)
    await application.process_update(update)
    return Response(status_code=200, content="OK")


@app.post("/health")
async def health() -> Response:
    return Response(status_code=200, content="OK")


# Установка вебхука при старте приложения
@app.on_event("startup")
async def on_startup() -> None:
    # Установка вебхука
    logger.info("Settings")
    logger.info(app_settings.model_dump_json(indent=4))
    if await application.bot.set_webhook(app_settings.telegram.webhook.unicode_string() + "webhook"):
        await application.initialize()
        await setup_commands(application)
        logger.info("Webhook set")
    else:
        logger.info("Webhook not set")


if __name__ == "__main__":
    container = AppContainer()
    uvicorn.run(app, host="0.0.0.0", port=app_settings.port)
