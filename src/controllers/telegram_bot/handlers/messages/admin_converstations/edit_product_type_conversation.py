import asyncio

import sqlalchemy as sa
from dependency_injector.wiring import Provide, inject
from loguru import logger
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import async_sessionmaker
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes, ConversationHandler

from src.constants import (
    ADD_NEW_PRODUCT_TYPE_MESSAGE_TEMPLATE,
    CANCEL_BUTTON_TEXT,
    DELETE_PRODUCT_TYPE_MESSAGE_TEMPLATE,
    EDIT_PRODUCT_TYPE_NAME_MESSAGE_TEMPLATE,
    PRODUCT_TYPE_EDIT_ACTIONS_BUTTONS_TEXT,
    SELECT_ACTION_MESSAGE_TEMPLATE,
)
from src.constants.templates.callback_templates import CANCEL_BUTTON_CALLBACK, PRODUCT_TYPE_ACTION_CALLBACK_TEMPLATE
from src.container import AppContainer
from src.controllers.telegram_bot.states import EDIT_PRODUCT_TYPE_NAME_STATE, SELECT_PRODUCT_TYPE_ACTION_STATE
from src.controllers.telegram_bot.utils.get_callback_query import get_callback_query
from src.enums import ProductTypeActionEnum
from src.gateways.database.models import Product, ProductType

_product_type_cache: dict[str, int | None] = {"product_type_id": None}


async def get_product_type_for_next_action_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> int:
    logger.info("Выбран продукт для редактирования. Предоставления выбора действий")
    query = await get_callback_query(update)
    product_type_id = query.data.split("_")[-1]
    await context.bot.send_message(
        text=SELECT_ACTION_MESSAGE_TEMPLATE,
        chat_id=update.effective_message.chat_id,
        reply_markup=InlineKeyboardMarkup(
            [
                (
                    InlineKeyboardButton(
                        action,
                        callback_data=PRODUCT_TYPE_ACTION_CALLBACK_TEMPLATE + str(i) + "_" + product_type_id,
                    ),
                )
                for i, action in enumerate(PRODUCT_TYPE_EDIT_ACTIONS_BUTTONS_TEXT)
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
    return SELECT_PRODUCT_TYPE_ACTION_STATE


@inject
async def get_product_type_action_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    session: async_sessionmaker = Provide[AppContainer.session_maker],
) -> int:
    logger.info("Выбрано действие редактирования продукта. Отправка сообщения для редактирования значения")
    query = await get_callback_query(update)
    callback_data = query.data.split("_")
    action, product_type_id = (
        int(callback_data[-2]),
        int(callback_data[-1]),
    )
    match action:
        case ProductTypeActionEnum.edit_name:
            await context.bot.send_message(
                text=ADD_NEW_PRODUCT_TYPE_MESSAGE_TEMPLATE,
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
            _product_type_cache["product_type_id"] = product_type_id
            return EDIT_PRODUCT_TYPE_NAME_STATE
        case ProductTypeActionEnum.delete_product_type:
            async with session() as _session:
                await _session.execute(delete(Product).where(Product.product_type_id == product_type_id))
                await _session.execute(delete(ProductType).where(ProductType.id == product_type_id))
                await asyncio.gather(
                    *(
                        context.bot.send_message(
                            text=DELETE_PRODUCT_TYPE_MESSAGE_TEMPLATE,
                            chat_id=update.effective_message.chat_id,
                        ),
                        _session.commit(),
                    )
                )
                return ConversationHandler.END


@inject
async def edit_product_type_name(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    session: async_sessionmaker = Provide[AppContainer.session_maker],
) -> int:
    logger.info("Изменение имени группы продуктов")
    new_product_type_name = update.message.text
    async with session() as _session:
        await _session.execute(
            sa.update(ProductType)
            .where(ProductType.id == _product_type_cache["product_type_id"])
            .values(name=new_product_type_name)
        )
        await asyncio.gather(
            *(
                context.bot.send_message(
                    text=EDIT_PRODUCT_TYPE_NAME_MESSAGE_TEMPLATE.format(product_type_name=new_product_type_name),
                    chat_id=update.effective_message.chat_id,
                ),
                _session.commit(),
            )
        )
        return ConversationHandler.END
