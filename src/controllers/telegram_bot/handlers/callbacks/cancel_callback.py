from loguru import logger
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from src.controllers.telegram_bot.utils.get_callback_query import get_callback_query_with_delete_message


async def get_cancel_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,  # noqa: ARG001
) -> int:
    logger.info("Обработка кнопки отмены")
    await get_callback_query_with_delete_message(update)
    return ConversationHandler.END
