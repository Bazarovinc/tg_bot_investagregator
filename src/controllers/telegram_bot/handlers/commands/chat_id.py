from loguru import logger
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from src.controllers.telegram_bot.utils.admin_virfication import verify_chat_id
from src.settings.app import app_settings


@verify_chat_id(app_settings.telegram.master_id)
async def get_chat_id_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,  # noqa: ARG001
) -> int:
    logger.info("Запущена команда /chat_id")
    await update.message.reply_text(f"chat_id={update.message.chat_id}")
    return ConversationHandler.END
