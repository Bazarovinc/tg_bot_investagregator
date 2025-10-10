from loguru import logger
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from src.constants import START_COMMAND_MESSAGE


async def get_start_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,  # noqa: ARG001
) -> int:
    logger.info("Запущена команда /start")
    await update.message.reply_text(START_COMMAND_MESSAGE)
    return ConversationHandler.END
