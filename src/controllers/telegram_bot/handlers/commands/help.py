from loguru import logger
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from src.constants import HELP_COMMAND_MESSAGE


async def get_help_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,  # noqa: ARG001
) -> int:
    logger.info("Запущена команда /help")
    await update.message.reply_text(
        HELP_COMMAND_MESSAGE,
    )
    return ConversationHandler.END
