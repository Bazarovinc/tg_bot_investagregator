from collections.abc import Callable, Coroutine
from typing import Any

from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from src.settings.app import app_settings


def check_admins(func: Callable[..., Coroutine[Any, Any, Any]]) -> Callable[..., Coroutine[Any, Any, Any]]:
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args: Any, **kwargs: Any) -> int:
        if update.effective_chat.id == app_settings.telegram.admin_chat_id:
            return await func(update, context, *args, **kwargs)
        return ConversationHandler.END

    return wrapper
