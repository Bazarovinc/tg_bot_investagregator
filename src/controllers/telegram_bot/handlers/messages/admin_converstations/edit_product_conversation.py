import asyncio
from decimal import Decimal

import sqlalchemy as sa
from dependency_injector.wiring import Provide, inject
from loguru import logger
from sqlalchemy.ext.asyncio import async_sessionmaker
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes, ConversationHandler

from src.constants import (
    ADD_PRODUCT_NEW_AGENT_PROFITABILITY_MESSAGE_TEMPLATE,
    ADD_PRODUCT_NEW_DESCRIPTION_MESSAGE_TEMPLATE,
    ADD_PRODUCT_NEW_NAME_MESSAGE_TEMPLATE,
    ADD_PRODUCT_NEW_PLACEMENT_PERIOD_MESSAGE_TEMPLATE,
    ADD_PRODUCT_NEW_PROFITABILITY_MESSAGE_TEMPLATE,
    CANCEL_BUTTON_CALLBACK,
    CANCEL_BUTTON_TEXT,
    PRODUCT_ACTION_CALLBACK_TEMPLATE,
    PRODUCT_EDIT_ACTIONS_BUTTONS_TEXT,
    PRODUCT_FOR_EDIT_CALLBACK_TEMPLATE,
    SELECT_PRODUCT_FOR_EDIT_MESSAGE_TEMPLATE,
)
from src.constants.templates.message_templates import (
    ADD_PRODUCT_NEW_FILE_MESSAGE_TEMPLATE,
    DELETE_PRODUCT_MESSAGE_TEMPLATE,
    EDIT_PRODUCT_AGENT_PROFITABILITY_MESSAGE_TEMPLATE,
    EDIT_PRODUCT_DESCRIPTION_MESSAGE_TEMPLATE,
    EDIT_PRODUCT_FILE_MESSAGE_TEMPLATE,
    EDIT_PRODUCT_NAME_MESSAGE_TEMPLATE,
    EDIT_PRODUCT_PLACEMENT_PERIOD_MESSAGE_TEMPLATE,
    EDIT_PRODUCT_PROFITABILITY_MESSAGE_TEMPLATE,
    SELECT_ACTION_MESSAGE_TEMPLATE,
)
from src.container import AppContainer
from src.controllers.telegram_bot.states import (
    EDIT_PRODUCT_AGENT_PROFITABILITY_STATE,
    EDIT_PRODUCT_DESCRIPTION_STATE,
    EDIT_PRODUCT_FILE_PATH_STATE,
    EDIT_PRODUCT_NAME_STATE,
    EDIT_PRODUCT_PLACEMENT_PERIOD_STATE,
    EDIT_PRODUCT_PROFITABILITY_STATE,
    SELECT_PRODUCT_ACTION_STATE,
    SELECT_PRODUCT_FOR_EDIT_STATE,
)
from src.controllers.telegram_bot.utils.get_callback_query import get_callback_query
from src.enums import ProductActionEnum
from src.gateways.database.models import Product
from src.gateways.object_storage_client import ObjectStorageClient

_product_cache: dict[str, int | None] = {"product_id": None}


@inject
async def get_product_type_for_product_selection_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    session: async_sessionmaker = Provide[AppContainer.session_maker],
) -> int:
    logger.info("Выбрана группа продуктов для редактирования продукта. Предоставления выбора продуктов")
    query = await get_callback_query(update)
    product_type_id = int(query.data.split("_")[-1])
    async with session() as _session:
        products = (
            (await _session.execute(sa.select(Product).where(Product.product_type_id == product_type_id)))
            .scalars()
            .all()
        )
        await context.bot.send_message(
            text=SELECT_PRODUCT_FOR_EDIT_MESSAGE_TEMPLATE,
            chat_id=update.effective_message.chat_id,
            reply_markup=InlineKeyboardMarkup(
                [
                    (
                        InlineKeyboardButton(
                            product.name,
                            callback_data=PRODUCT_FOR_EDIT_CALLBACK_TEMPLATE + str(product.id),
                        ),
                    )
                    for product in products
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
    return SELECT_PRODUCT_FOR_EDIT_STATE


async def _send_action_selection(
    product_id: str,
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    await context.bot.send_message(
        text=SELECT_ACTION_MESSAGE_TEMPLATE,
        chat_id=update.effective_message.chat_id,
        reply_markup=InlineKeyboardMarkup(
            [
                (
                    InlineKeyboardButton(
                        action,
                        callback_data=PRODUCT_ACTION_CALLBACK_TEMPLATE + str(i) + "_" + product_id,
                    ),
                )
                for i, action in enumerate(PRODUCT_EDIT_ACTIONS_BUTTONS_TEXT)
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


async def get_product_callback_and_send_action_selection(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    logger.info("Выбран продукт для редактирования. Предоставления выбора действий")
    query = await get_callback_query(update)
    product_id = query.data.split("_")[-1]
    await _send_action_selection(product_id, update, context)
    return SELECT_PRODUCT_ACTION_STATE


@inject
async def get_action_callback(  # noqa: PLR0911
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    session: async_sessionmaker = Provide[AppContainer.session_maker],
) -> int:
    logger.info("Выбрано действие редактирования продукта. Отправка сообщения для редактирования значения")
    query = await get_callback_query(update)
    callback_data = query.data.split("_")
    action, product_id = (
        int(callback_data[-2]),
        int(callback_data[-1]),
    )
    _product_cache["product_id"] = product_id
    match action:
        case ProductActionEnum.edit_name:
            await context.bot.send_message(
                text=ADD_PRODUCT_NEW_NAME_MESSAGE_TEMPLATE,
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
            return EDIT_PRODUCT_NAME_STATE
        case ProductActionEnum.edit_profitability:
            await context.bot.send_message(
                text=ADD_PRODUCT_NEW_PROFITABILITY_MESSAGE_TEMPLATE,
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
            print("State", EDIT_PRODUCT_PROFITABILITY_STATE)
            return EDIT_PRODUCT_PROFITABILITY_STATE
        case ProductActionEnum.edit_agent_profitability:
            await context.bot.send_message(
                text=ADD_PRODUCT_NEW_AGENT_PROFITABILITY_MESSAGE_TEMPLATE,
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
            print("State", EDIT_PRODUCT_AGENT_PROFITABILITY_STATE)
            return EDIT_PRODUCT_AGENT_PROFITABILITY_STATE
        case ProductActionEnum.edit_placement_period:
            await context.bot.send_message(
                text=ADD_PRODUCT_NEW_PLACEMENT_PERIOD_MESSAGE_TEMPLATE,
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
            print("State", EDIT_PRODUCT_PLACEMENT_PERIOD_STATE)
            return EDIT_PRODUCT_PLACEMENT_PERIOD_STATE
        case ProductActionEnum.edit_description:
            await context.bot.send_message(
                text=ADD_PRODUCT_NEW_DESCRIPTION_MESSAGE_TEMPLATE,
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
            print(" State", EDIT_PRODUCT_DESCRIPTION_STATE)
            return EDIT_PRODUCT_DESCRIPTION_STATE
        case ProductActionEnum.edit_file_path:
            await context.bot.send_message(
                text=ADD_PRODUCT_NEW_FILE_MESSAGE_TEMPLATE,
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
            print(" State", EDIT_PRODUCT_FILE_PATH_STATE)
            return EDIT_PRODUCT_FILE_PATH_STATE
        case ProductActionEnum.delete_product:
            async with session() as _session:
                await _session.execute(sa.delete(Product).where(Product.id == product_id))
                await asyncio.gather(
                    *(
                        context.bot.send_message(
                            text=DELETE_PRODUCT_MESSAGE_TEMPLATE,
                            chat_id=update.effective_message.chat_id,
                        ),
                        _session.commit(),
                    )
                )
                return ConversationHandler.END


@inject
async def _edit_new_value_and_send_edit_selection(
    new_value: dict[str, str | int],
    message: str,
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    session: async_sessionmaker = Provide[AppContainer.session_maker],
) -> int:
    product_id = _product_cache["product_id"]
    async with session() as _session:
        await _session.execute(sa.update(Product).where(Product.id == product_id).values(**new_value))
        await asyncio.gather(
            *(
                context.bot.send_message(
                    text=message,
                    chat_id=update.effective_message.chat_id,
                ),
                _session.commit(),
                _send_action_selection(str(product_id), update, context),
            )
        )
    return SELECT_PRODUCT_ACTION_STATE


async def edit_product_name(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    field_name: str = "name",
    message: str = EDIT_PRODUCT_NAME_MESSAGE_TEMPLATE,
) -> int:
    logger.info("Изменение имени продукта")
    value = update.message.text
    return await _edit_new_value_and_send_edit_selection(
        {field_name: value}, message.format(value=value), update, context
    )


async def edit_product_profitability(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    field_name: str = "profitability",
    message: str = EDIT_PRODUCT_PROFITABILITY_MESSAGE_TEMPLATE,
) -> int:
    logger.info("Изменение «Доходности по продукту»")
    value = int(Decimal(update.message.text.replace(",", ".")) * 100)
    return await _edit_new_value_and_send_edit_selection(
        {field_name: value}, message.format(value=value), update, context
    )


async def edit_product_agent_profitability(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    field_name: str = "agent_profitability",
    message: str = EDIT_PRODUCT_AGENT_PROFITABILITY_MESSAGE_TEMPLATE,
) -> int:
    logger.info("Изменение «Доходности для агента»")
    value = int(Decimal(update.message.text.replace(",", ".")) * 100)
    return await _edit_new_value_and_send_edit_selection(
        {field_name: value}, message.format(value=value), update, context
    )


async def edit_product_placement_period(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    field_name: str = "placement_period",
    message: str = EDIT_PRODUCT_PLACEMENT_PERIOD_MESSAGE_TEMPLATE,
) -> int:
    logger.info("Изменение «Срока продукта»")
    value = int(update.message.text)
    return await _edit_new_value_and_send_edit_selection(
        {field_name: value}, message.format(value=value), update, context
    )


async def edit_product_description(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    field_name: str = "description",
    message: str = EDIT_PRODUCT_DESCRIPTION_MESSAGE_TEMPLATE,
) -> int:
    logger.info("Изменение описания")
    value = update.message.text
    return await _edit_new_value_and_send_edit_selection({field_name: value}, message, update, context)


@inject
async def edit_file_path(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    session: async_sessionmaker = Provide[AppContainer.session_maker],
    object_storage: ObjectStorageClient = Provide[AppContainer.object_storage],
    message: str = EDIT_PRODUCT_FILE_MESSAGE_TEMPLATE,
) -> int:
    logger.info("Сохранение нового файла и удаление старого")
    product_id = _product_cache["product_id"]
    async with session() as _session:
        document = update.message.document
        file_id = document.file_id
        file_name = document.file_name
        select_result, file = await asyncio.gather(
            *(_session.execute(sa.select(Product).where(Product.id == product_id)), context.bot.get_file(file_id))
        )
        product: Product = select_result.scalar_one()
        file_bytes = await file.download_as_bytearray()
        file_path = f"products/{product.product_type_id}/{product.name}/{file_name}"
        _tasks = (
            (
                object_storage.delete_file(product.file_path),
                object_storage.save_file(file_bytes, file_path),
                _session.execute(sa.update(Product).where(Product.id == product_id).values(file_path=file_path)),
            )
            if product.file_path
            else (
                object_storage.save_file(file_bytes, file_path),
                _session.execute(sa.update(Product).where(Product.id == product_id).values(file_path=file_path)),
            )
        )
        await asyncio.gather(*_tasks)
        await asyncio.gather(
            *(
                context.bot.send_message(
                    text=message,
                    chat_id=update.effective_message.chat_id,
                ),
                _session.commit(),
                _send_action_selection(str(product_id), update, context),
            )
        )
    return SELECT_PRODUCT_ACTION_STATE
