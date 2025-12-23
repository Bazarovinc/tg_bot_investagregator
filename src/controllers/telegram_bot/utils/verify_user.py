from collections.abc import Callable, Coroutine
from typing import Any, TypeVar

from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from src.constants import NOT_CHANEL_USER_STATUSES
from src.settings.app import app_settings

HandlerReturnType = TypeVar("HandlerReturnType")
AsyncHandlerFunc = Callable[..., Coroutine[Any, Any, HandlerReturnType]]


def verify_user(func: AsyncHandlerFunc[HandlerReturnType]) -> AsyncHandlerFunc[int]:
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *_args: Any, **_kwargs: Any) -> int:
        chat_member = await context.bot.get_chat_member(app_settings.telegram.guard_chanel_id, update.effective_user.id)
        if chat_member.status not in NOT_CHANEL_USER_STATUSES:
            return await func(update, context, *_args, **_kwargs)
        return ConversationHandler.END

    return wrapper
