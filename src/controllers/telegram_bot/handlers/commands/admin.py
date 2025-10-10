from loguru import logger
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from src.constants import (
    ADMIN_BUTTONS_TEXT,
    ADMIN_CALLBACK_TEMPLATE,
    ADMIN_MESSAGE_TEMPLATE,
    CANCEL_BUTTON_CALLBACK,
    CANCEL_BUTTON_TEXT,
)
from src.controllers.telegram_bot.states import ADMIN_START_STATE
from src.controllers.telegram_bot.utils.admin_virfication import check_admins


@check_admins
async def get_admin_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,  # noqa: ARG001
) -> int:
    logger.info("Запущена команда /admin")
    await context.bot.send_message(
        text=ADMIN_MESSAGE_TEMPLATE,
        chat_id=update.effective_message.chat_id,
        reply_markup=InlineKeyboardMarkup(
            [
                (InlineKeyboardButton(admin_button_text, callback_data=ADMIN_CALLBACK_TEMPLATE + str(i)),)
                for i, admin_button_text in enumerate(ADMIN_BUTTONS_TEXT)
            ]
            + [
                (
                    InlineKeyboardButton(
                        CANCEL_BUTTON_TEXT,
                        callback_data=CANCEL_BUTTON_CALLBACK,
                    ),
                )
            ]
        ),
    )

    return ADMIN_START_STATE
