from collections.abc import Callable, Coroutine
from typing import Any, TypeVar

from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

HandlerReturnType = TypeVar("HandlerReturnType")
AsyncHandlerFunc = Callable[..., Coroutine[Any, Any, HandlerReturnType]]


def verify_chat_id(chat_id: int) -> Callable[[AsyncHandlerFunc[HandlerReturnType]], AsyncHandlerFunc[int]]:
    def wrapper(func: AsyncHandlerFunc[HandlerReturnType]) -> AsyncHandlerFunc[int]:
        async def inner_wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args: Any, **kwargs: Any) -> int:
            print(update.effective_chat.id)
            if update.effective_chat.id == chat_id:
                return await func(update, context, *args, **kwargs)
            return ConversationHandler.END

        return inner_wrapper

    return wrapper
