import asyncio
from datetime import datetime
from zoneinfo import ZoneInfo

from dependency_injector.wiring import Provide, inject
from loguru import logger
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import async_sessionmaker
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from src.constants import (
    FINISH_BUTTON_TEXT,
    FINISH_SUPPORT_DIALOG_CALLBACK,
    SUPPORT_START_MESSAGE_TEMPLATE,
)
from src.container import AppContainer
from src.controllers.telegram_bot.states import START_SUPPORT_STATE
from src.controllers.telegram_bot.utils.verify_user import verify_user
from src.gateways.database.models import SupportDialog


@verify_user
@inject
async def get_support_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,  # noqa: ARG001
    session: async_sessionmaker = Provide[AppContainer.session_maker],
) -> int:
    logger.info("Запущена команда /support")
    user = update.message.from_user
    async with session() as _session:
        today = datetime.now(tz=ZoneInfo("Europe/Moscow")).date()
        _query = select(func.max(SupportDialog.daily_dialog_count)).where(SupportDialog.dialog_date == today)
        result = await _session.execute(_query)
        current_daily_dialog_count = result.scalar() or 0
        current_daily_dialog_count += 1
        dialog_id = int(f"{today.year}{today.month}{today.day}{current_daily_dialog_count}")

        new_support_dialog = SupportDialog(
            id=dialog_id, daily_dialog_count=current_daily_dialog_count, dialog_date=today, user_id=user.id
        )
        _session.add(new_support_dialog)

        await asyncio.gather(
            *(
                context.bot.send_message(
                    text=SUPPORT_START_MESSAGE_TEMPLATE,
                    chat_id=update.effective_message.chat_id,
                    reply_markup=InlineKeyboardMarkup(
                        [
                            (
                                InlineKeyboardButton(
                                    FINISH_BUTTON_TEXT,
                                    callback_data=FINISH_SUPPORT_DIALOG_CALLBACK,
                                ),
                            )
                        ]
                    ),
                ),
                _session.commit(),
            )
        )
    return START_SUPPORT_STATE
