import asyncio
from decimal import Decimal
from typing import TypedDict

from dependency_injector.wiring import Provide, inject
from loguru import logger
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes, ConversationHandler

from src.constants import (
    ADD_NEW_PRODUCT_AGENT_PROFITABILITY_MESSAGE_TEMPLATE,
    ADD_NEW_PRODUCT_DESCRIPTION_MESSAGE_TEMPLATE,
    ADD_NEW_PRODUCT_FILE_MESSAGE_TEMPLATE,
    ADD_NEW_PRODUCT_PLACEMENT_PERIOD_MESSAGE_TEMPLATE,
    ADD_NEW_PRODUCT_PROFITABILITY_MESSAGE_TEMPLATE,
    CANCEL_BUTTON_CALLBACK,
    FINISH_BUTTON_TEXT,
    MISSING_VALUE,
    PRODUCT_SAVED_MESSAGE_TEMPLATE,
    SET_PRODUCT_TYPE_FOR_NEW_PRODUCT_MESSAGE_TEMPLATE,
    SKIPP_BUTTON_TEXT,
)
from src.constants.templates import (
    CANCEL_BUTTON_TEXT,
    FINISH_CALLBACK_TEMPLATE,
    PRODUCT_TYPE_FOR_NEW_PRODUCT_CALLBACK_TEMPLATE,
    SKIPP_CALLBACK_TEMPLATE,
)
from src.container import AppContainer
from src.controllers.telegram_bot.states import (
    ADD_PRODUCT_AGENT_PROFITABILITY_STATE,
    ADD_PRODUCT_DESCRIPTION_STATE,
    ADD_PRODUCT_FILE_STATE,
    ADD_PRODUCT_PLACEMENT_PERIOD_STATE,
    ADD_PRODUCT_PROFITABILITY_STATE,
    ADD_PRODUCT_TYPE_STATE,
)
from src.controllers.telegram_bot.utils.get_callback_query import get_callback_query
from src.gateways.database.models import Product, ProductType
from src.gateways.object_storage_client import ObjectStorageClient


class ProductCacheData(TypedDict):
    name: str | None
    profitability: int | None
    agent_profitability: int | None
    placement_period: int | None
    product_type_id: int | None
    description: str | None
    file_path: str | None


_product_cache: ProductCacheData = ProductCacheData(
    name=None,
    profitability=None,
    agent_profitability=None,
    placement_period=None,
    product_type_id=None,
    description=None,
    file_path=None,
)


def _renew_product_cache() -> None:
    _product_cache = ProductCacheData(
        name=None,
        profitability=None,
        agent_profitability=None,
        placement_period=None,
        product_type_id=None,
        description=None,
        file_path=None,
    )


@inject
async def add_product_name_and_send_next_question(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    session: async_sessionmaker = Provide[AppContainer.session_maker],
) -> int:
    logger.info("Добавлено имя нового продукта. Предоставлен выбор группы продуктов")
    product_name = update.message.text
    print(product_name)
    _renew_product_cache()
    _product_cache["name"] = product_name
    async with session() as _session:
        product_types = (await _session.execute(select(ProductType))).scalars().all()
        await context.bot.send_message(
            text=SET_PRODUCT_TYPE_FOR_NEW_PRODUCT_MESSAGE_TEMPLATE,
            chat_id=update.effective_message.chat_id,
            reply_markup=InlineKeyboardMarkup(
                [
                    (
                        InlineKeyboardButton(
                            product_type.name,
                            callback_data=PRODUCT_TYPE_FOR_NEW_PRODUCT_CALLBACK_TEMPLATE + str(product_type.id),
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
    return ADD_PRODUCT_TYPE_STATE


async def get_product_type_id_callback_and_send_next_question(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> int:
    logger.info("Добавлена группа продуктов нового продукта. Запрос «Доходности по продукту»")
    query = await get_callback_query(update)
    product_type_id = int(query.data.split("_")[-1])
    _product_cache["product_type_id"] = product_type_id
    await context.bot.send_message(
        text=ADD_NEW_PRODUCT_PROFITABILITY_MESSAGE_TEMPLATE,
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
    return ADD_PRODUCT_PROFITABILITY_STATE


async def add_product_profitability_and_send_next_question(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> int:
    logger.info("Добавлена «Доходность по продукту» нового продукта. Запрос «Доходности для агента»")
    product_profitability = int(Decimal(update.message.text.replace(",", ".")) * 100)
    _product_cache["profitability"] = product_profitability
    await context.bot.send_message(
        text=ADD_NEW_PRODUCT_AGENT_PROFITABILITY_MESSAGE_TEMPLATE,
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
    return ADD_PRODUCT_AGENT_PROFITABILITY_STATE


async def add_product_agent_profitability_and_send_next_question(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> int:
    logger.info("Добавлена «Доходность для агента» нового продукта. Запрос «Срока продукта»")
    product_agent_profitability = int(Decimal(update.message.text.replace(",", ".")) * 100)
    _product_cache["agent_profitability"] = product_agent_profitability
    await context.bot.send_message(
        text=ADD_NEW_PRODUCT_PLACEMENT_PERIOD_MESSAGE_TEMPLATE,
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
    return ADD_PRODUCT_PLACEMENT_PERIOD_STATE


async def add_product_placement_period_state_and_send_next_question(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> int:
    logger.info("Добавлена «Срок продукта» нового продукта. Запрос описания")
    placement_period = int(update.message.text)
    _product_cache["placement_period"] = placement_period
    await context.bot.send_message(
        text=ADD_NEW_PRODUCT_DESCRIPTION_MESSAGE_TEMPLATE,
        chat_id=update.effective_message.chat_id,
        reply_markup=InlineKeyboardMarkup(
            [
                (
                    InlineKeyboardButton(
                        SKIPP_BUTTON_TEXT,
                        callback_data=SKIPP_CALLBACK_TEMPLATE,
                    ),
                ),
                (
                    InlineKeyboardButton(
                        CANCEL_BUTTON_TEXT,
                        callback_data=CANCEL_BUTTON_CALLBACK,
                    ),
                ),
            ]
        ),
    )
    return ADD_PRODUCT_DESCRIPTION_STATE


async def _send_message_about_new_product_file(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> int:
    await context.bot.send_message(
        text=ADD_NEW_PRODUCT_FILE_MESSAGE_TEMPLATE,
        chat_id=update.effective_message.chat_id,
        reply_markup=InlineKeyboardMarkup(
            [
                (
                    InlineKeyboardButton(
                        FINISH_BUTTON_TEXT,
                        callback_data=FINISH_CALLBACK_TEMPLATE,
                    ),
                ),
                (
                    InlineKeyboardButton(
                        CANCEL_BUTTON_TEXT,
                        callback_data=CANCEL_BUTTON_CALLBACK,
                    ),
                ),
            ]
        ),
    )
    return ADD_PRODUCT_FILE_STATE


async def get_product_description_skipp_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    logger.info("Описание нового продукта пропущено. Запрос файла")
    _product_cache["description"] = None
    await get_callback_query(update)
    return await _send_message_about_new_product_file(update, context)


async def add_product_description_and_send_next_question(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> int:
    logger.info("Добавлено описание нового продукта. Запрос файла")
    description = update.message.text
    _product_cache["description"] = description
    return await _send_message_about_new_product_file(update, context)


@inject
async def _save_new_product_and_send_finish_message(
    file_name: str,
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    session: async_sessionmaker = Provide[AppContainer.session_maker],
) -> int:
    async with session() as _session:
        product_type: ProductType = (
            (await _session.execute(select(ProductType).where(ProductType.id == _product_cache["product_type_id"])))
            .scalars()
            .one()
        )
        _session.add(Product(**_product_cache))
        await asyncio.gather(
            *(
                _session.commit(),
                context.bot.send_message(
                    text=PRODUCT_SAVED_MESSAGE_TEMPLATE.format(
                        name=_product_cache["name"],
                        profitability=round(Decimal(_product_cache["profitability"] / 100), 2),
                        agent_profitability=round(Decimal(_product_cache["agent_profitability"] / 100), 2),
                        placement_period=_product_cache["placement_period"],
                        product_type=product_type.name,
                        description=_product_cache["description"] or MISSING_VALUE,
                        file_name=file_name,
                    ),
                    chat_id=update.effective_message.chat_id,
                ),
            )
        )
    return ConversationHandler.END


async def get_finish_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    logger.info("Добавление файла нового продукта пропущено. Завершение")
    _product_cache["file_path"] = None
    await get_callback_query(update)
    return await _save_new_product_and_send_finish_message(MISSING_VALUE, update, context)


@inject
async def add_product_file_and_save_product(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    object_storage: ObjectStorageClient = Provide[AppContainer.object_storage],
) -> int:
    logger.info("Добавление файла нового продукта. Сохранение файла. Завершение")
    document = update.message.document
    file_id = document.file_id
    file_name = document.file_name
    file = await context.bot.get_file(file_id)
    file_bytes = await file.download_as_bytearray()
    file_path = f"products/{_product_cache['product_type_id']}/{_product_cache['name']}/{file_name}"
    await object_storage.save_file(file_bytes, file_path)
    _product_cache["file_path"] = file_path
    return await _save_new_product_and_send_finish_message(file_name, update, context)
