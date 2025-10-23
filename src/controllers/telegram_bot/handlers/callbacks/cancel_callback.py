import asyncio

import sqlalchemy as sa
from dependency_injector.wiring import Provide, inject
from loguru import logger
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import async_sessionmaker
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from src.constants import (
    SUPPORT_DIALOG_FINISH_MESSAGE_TEMPLATE,
    SUPPORT_DIALOG_FINISHED_BY_SUPPORT_MESSAGE_TEMPLATE,
    SUPPORT_DIALOG_FINISHED_BY_USER_MESSAGE_TEMPLATE,
    SUPPORT_DIALOG_FINISHED_MESSAGE_TEMPLATE,
    SUPPORT_DIALOG_ID_PATTERN,
)
from src.container import AppContainer
from src.controllers.telegram_bot.utils.get_callback_query import (
    get_callback_query,
    get_callback_query_with_delete_message,
)
from src.enums import SupportDialogStatusEnum
from src.gateways.database.models import SupportDialog
from src.settings.app import app_settings


async def get_cancel_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,  # noqa: ARG001
) -> int:
    logger.info("Обработка кнопки отмены")
    await get_callback_query_with_delete_message(update)
    return ConversationHandler.END


@inject
async def get_finish_conversation_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,  # noqa: ARG001
    session: async_sessionmaker = Provide[AppContainer.session_maker],
) -> int:
    logger.info("Обработка кнопки завершения")

    query = await get_callback_query(update)
    async with session() as _session:
        if match := SUPPORT_DIALOG_ID_PATTERN.search(query.message.text):
            dialog_id = int(match.group(1))
            support_dialog_info: SupportDialog = (
                await _session.execute(select(SupportDialog).where(SupportDialog.id == dialog_id))
            ).scalar_one()
            support_dialog_info.status = SupportDialogStatusEnum.finished_by_support
            user_message, support_message = (
                SUPPORT_DIALOG_FINISHED_BY_SUPPORT_MESSAGE_TEMPLATE,
                SUPPORT_DIALOG_FINISH_MESSAGE_TEMPLATE.format(dialog_id=support_dialog_info.id),
            )
        else:
            user_id = query.message.chat.id
            support_dialog_info: SupportDialog = (
                (
                    await _session.execute(
                        select(SupportDialog)
                        .where(
                            SupportDialog.user_id == user_id,
                            SupportDialog.status.in_(
                                (SupportDialogStatusEnum.started, SupportDialogStatusEnum.in_progress)
                            ),
                        )
                        .order_by(desc(SupportDialog.daily_dialog_count))
                    )
                )
                .scalars()
                .first()
            )
            support_dialog_info.status = SupportDialogStatusEnum.finished_by_user
            user_message, support_message = (
                SUPPORT_DIALOG_FINISHED_MESSAGE_TEMPLATE,
                SUPPORT_DIALOG_FINISHED_BY_USER_MESSAGE_TEMPLATE.format(dialog_id=support_dialog_info.id),
            )

        await _session.execute(
            sa.update(SupportDialog)
            .values(status=support_dialog_info.status)
            .where(SupportDialog.id == support_dialog_info.id)
        )
        await asyncio.gather(
            *(
                _session.commit(),
                context.bot.send_message(
                    chat_id=support_dialog_info.user_id,
                    text=user_message,
                ),
                context.bot.send_message(
                    chat_id=app_settings.telegram.support_chat_id,
                    text=support_message,
                ),
            )
        )

    return ConversationHandler.END
