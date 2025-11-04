import asyncio

import sqlalchemy as sa
from dependency_injector.wiring import Provide, inject
from loguru import logger
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import async_sessionmaker
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes, ConversationHandler

from src.constants import (
    FINISH_BUTTON_TEXT,
    FINISH_SUPPORT_DIALOG_CALLBACK,
    SUPPORT_DIALOG_ANSWER_TO_USER_MESSAGE_TEMPLATE,
    SUPPORT_DIALOG_ID_PATTERN,
    SUPPORT_DIALOG_QUESTION_TO_SUPPORT_MESSAGE_TEMPLATE,
    USER_WITH_USERNAME,
    USER_WITHOUT_USERNAME,
)
from src.container import AppContainer
from src.controllers.telegram_bot.states import START_SUPPORT_STATE, SUPPORT_STATE
from src.enums import SupportDialogStatusEnum
from src.gateways.database.models import SupportDialog
from src.settings.app import app_settings


@inject
async def process_user_reply_to_support(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    session: async_sessionmaker = Provide[AppContainer.session_maker],
) -> int:
    logger.info("Вопрос пользователя")
    user = update.message.from_user
    user_message = update.message.text
    async with session() as _session:
        support_dialog_info: SupportDialog = (
            (
                await _session.execute(
                    select(SupportDialog)
                    .where(
                        SupportDialog.user_id == user.id,
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
        if support_dialog_info.status == SupportDialogStatusEnum.started:
            await _session.execute(
                sa.update(SupportDialog)
                .where(SupportDialog.id == support_dialog_info.id)
                .values(status=SupportDialogStatusEnum.in_progress)
            )
        await asyncio.gather(
            *(
                context.bot.send_message(
                    text=SUPPORT_DIALOG_QUESTION_TO_SUPPORT_MESSAGE_TEMPLATE.format(
                        dialog_id=support_dialog_info.id,
                        question=user_message,
                        user=USER_WITH_USERNAME.format(username=user.username)
                        if user.username
                        else USER_WITHOUT_USERNAME,
                    ),
                    chat_id=app_settings.telegram.support_chat_id,
                ),
                _session.commit(),
            )
        )
    return START_SUPPORT_STATE


@inject
async def process_support_reply_to_user(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    session: async_sessionmaker = Provide[AppContainer.session_maker],
) -> int:
    logger.info("Ответ поддержки")
    message = update.effective_message
    answer = message.text
    replied_message = message.reply_to_message.text
    if match := SUPPORT_DIALOG_ID_PATTERN.search(replied_message):
        dialog_id = int(match.group(1))
    else:
        return ConversationHandler.END
    async with session() as _session:
        support_dialog_info: SupportDialog = (
            await _session.execute(select(SupportDialog).where(SupportDialog.id == dialog_id))
        ).scalar_one()
        await context.bot.send_message(
            text=SUPPORT_DIALOG_ANSWER_TO_USER_MESSAGE_TEMPLATE.format(answer=answer),
            chat_id=support_dialog_info.user_id,
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
        )
    return SUPPORT_STATE
