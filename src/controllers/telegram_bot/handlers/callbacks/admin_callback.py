from dependency_injector.wiring import Provide, inject
from loguru import logger
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from src.constants import (
    ADD_NEW_PRODUCT_MESSAGE_TEMPLATE,
    ADD_NEW_PRODUCT_TYPE_MESSAGE_TEMPLATE,
    CANCEL_BUTTON_CALLBACK,
    CANCEL_BUTTON_TEXT,
    MENU_COMMAND_MESSAGE,
    PRODUCT_TYPE_FOR_EDIT_CALLBACK_TEMPLATE,
    PRODUCT_TYPE_FOR_PRODUCT_EDIT_CALLBACK_TEMPLATE,
    SELECT_PRODUCT_TYPE_FOR_EDIT_MESSAGE_TEMPLATE,
)
from src.container import AppContainer
from src.controllers.telegram_bot.states import (
    ADD_NEW_PRODUCT_TYPE_STATE,
    ADD_PRODUCT_NAME_STATE,
    ADMIN_START_STATE,
    SELECT_PRODUCT_TYPE_FOR_EDIT_PRODUCT_STATE,
    SELECT_PRODUCT_TYPE_FOR_EDIT_STATE,
)
from src.controllers.telegram_bot.utils.get_callback_query import get_callback_query
from src.enums import AdminActionEnum
from src.gateways.database.models import ProductType


@inject
async def get_admin_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    session: async_sessionmaker = Provide[AppContainer.session_maker],
) -> int | None:
    logger.info("Обработка кнопок администрирования")
    query = await get_callback_query(update)
    admin_action_id = int(query.data.split("_")[-1])
    print(admin_action_id)
    async with session() as _session:
        match admin_action_id:
            case AdminActionEnum.add_product_type:
                await query.edit_message_text(
                    text=ADD_NEW_PRODUCT_TYPE_MESSAGE_TEMPLATE,
                    reply_markup=InlineKeyboardMarkup(
                        [
                            (
                                InlineKeyboardButton(
                                    CANCEL_BUTTON_TEXT,
                                    callback_data=CANCEL_BUTTON_CALLBACK,
                                ),
                            )
                        ]
                    ),
                )
                # await context.bot.send_message(
                #
                # )
                return ADD_NEW_PRODUCT_TYPE_STATE
            case AdminActionEnum.add_product:
                await context.bot.send_message(
                    text=ADD_NEW_PRODUCT_MESSAGE_TEMPLATE,
                    chat_id=update.effective_message.chat_id,
                    reply_markup=InlineKeyboardMarkup(
                        [
                            (
                                InlineKeyboardButton(
                                    CANCEL_BUTTON_TEXT,
                                    callback_data=CANCEL_BUTTON_CALLBACK,
                                ),
                            )
                        ]
                    ),
                )
                return ADD_PRODUCT_NAME_STATE
            case AdminActionEnum.edit_product_type:
                product_types = (await _session.execute(select(ProductType))).scalars().all()
                await context.bot.send_message(
                    text=SELECT_PRODUCT_TYPE_FOR_EDIT_MESSAGE_TEMPLATE,
                    chat_id=update.effective_message.chat_id,
                    reply_markup=InlineKeyboardMarkup(
                        [
                            (
                                InlineKeyboardButton(
                                    product_type.name,
                                    callback_data=PRODUCT_TYPE_FOR_EDIT_CALLBACK_TEMPLATE + str(product_type.id),
                                ),
                            )
                            for product_type in product_types
                        ]
                        + [
                            (
                                InlineKeyboardButton(
                                    CANCEL_BUTTON_TEXT,
                                    callback_data=CANCEL_BUTTON_CALLBACK,
                                ),
                            )
                        ],
                    ),
                )
                return SELECT_PRODUCT_TYPE_FOR_EDIT_STATE
            case AdminActionEnum.edit_product:
                product_types = (await _session.execute(select(ProductType))).scalars().all()
                await context.bot.send_message(
                    text=MENU_COMMAND_MESSAGE,
                    chat_id=update.effective_message.chat_id,
                    reply_markup=InlineKeyboardMarkup(
                        [
                            (
                                InlineKeyboardButton(
                                    product_type.name,
                                    callback_data=PRODUCT_TYPE_FOR_PRODUCT_EDIT_CALLBACK_TEMPLATE
                                    + str(product_type.id),
                                ),
                            )
                            for product_type in product_types
                        ]
                        + [
                            (
                                InlineKeyboardButton(
                                    CANCEL_BUTTON_TEXT,
                                    callback_data=CANCEL_BUTTON_CALLBACK,
                                ),
                            )
                        ],
                    ),
                )
                return SELECT_PRODUCT_TYPE_FOR_EDIT_PRODUCT_STATE
    return ADMIN_START_STATE
