from dependency_injector.wiring import Provide, inject
from loguru import logger
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import async_sessionmaker
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes, ConversationHandler

from src.constants import (
    MENU_CALLBACK_MESSAGE_TEMPLATE,
    ORDERING_BUTTONS_TEXT,
    ORDERING_CALLBACK_TEMPLATE,
    PRODUCT_CALLBACK_TEMPLATE,
    PRODUCT_INFO_MESSAGE_TEMPLATE,
    PRODUCT_SELECT_MESSAGE_TEMPLATE,
)
from src.container import AppContainer
from src.controllers.telegram_bot.utils.get_callback_query import (
    get_callback_query,
    get_callback_query_with_delete_message,
)
from src.gateways.database.models import Product, ProductType
from src.gateways.object_storage_client import ObjectStorageClient


async def get_menu_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,  # noqa: ARG001
) -> None:
    logger.info("Выбрана группа продуктов. Предоставлен выбор сортировки")
    query = await get_callback_query(update)
    product_type_id = query.data.split("_")[-1]
    await query.edit_message_text(
        text=MENU_CALLBACK_MESSAGE_TEMPLATE,
        reply_markup=InlineKeyboardMarkup(
            [
                (
                    InlineKeyboardButton(
                        ordering_button_text, callback_data=ORDERING_CALLBACK_TEMPLATE + str(i) + "_" + product_type_id
                    ),
                )
                for i, ordering_button_text in enumerate(ORDERING_BUTTONS_TEXT)
            ]
        ),
    )


@inject
async def get_ordering_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,  # noqa: ARG001
    session: async_sessionmaker = Provide[AppContainer.session_maker],
) -> int:
    logger.info("Выбрана сортировка продуктов. Предоставлен выбор продукта")
    query = await get_callback_query(update)
    _, sort_field, product_type_id = query.data.split("_")

    async with session() as _session:
        _query = select(Product).where(Product.product_type_id == int(product_type_id))
        match int(sort_field):
            case 0:
                _query = _query.order_by(desc(Product.profitability).nulls_last())
            case 1:
                _query = _query.order_by(desc(Product.agent_profitability).nulls_last())
            case 2:
                _query = _query.order_by(desc(Product.placement_period).nulls_last())
        products = (await _session.execute(_query)).scalars().all()
        print(products)
        match int(sort_field):
            case 0:
                buttons = [
                    (
                        InlineKeyboardButton(
                            f"{product.name} ({product.profitability_readable}{'%' if product.profitability else ''})",
                            callback_data=PRODUCT_CALLBACK_TEMPLATE + str(product.id),
                        ),
                    )
                    for product in products
                ]
            case 1:
                buttons = [
                    (
                        InlineKeyboardButton(
                            f"{product.name} ({product.agent_profitability_readable}"
                            f"{'%' if product.agent_profitability else ''})",
                            callback_data=PRODUCT_CALLBACK_TEMPLATE + str(product.id),
                        ),
                    )
                    for product in products
                ]
            case 2:
                buttons = [
                    (
                        InlineKeyboardButton(
                            f"{product.name} ({product.placement_period_readable}"
                            f"{' год/лет' if product.placement_period else ''})",
                            callback_data=PRODUCT_CALLBACK_TEMPLATE + str(product.id),
                        ),
                    )
                    for product in products
                ]
        await query.edit_message_text(
            text=PRODUCT_SELECT_MESSAGE_TEMPLATE,
            reply_markup=InlineKeyboardMarkup(buttons),
        )


@inject
async def get_product_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    session: async_sessionmaker = Provide[AppContainer.session_maker],
    object_storage: ObjectStorageClient = Provide[AppContainer.object_storage],
) -> int:
    logger.info("Выбран продукт. Предоставлена информация по продукту")
    query = await get_callback_query_with_delete_message(update)
    product_id = int(query.data.split("_")[-1])
    async with session() as _session:
        product: Product = (await _session.execute(select(Product).where(Product.id == product_id))).scalars().one()
        if product.description:
            await context.bot.send_message(
                text=product.description,
                chat_id=update.effective_chat.id,
            )
        if product.file_path:
            file = await object_storage.get_file(product.file_path)
            await context.bot.send_document(
                chat_id=update.effective_chat.id, document=file, filename=product.file_path.split("/")[-1]
            )
        if not product.description and not product.file_path:
            product_type: ProductType = (
                (await _session.execute(select(ProductType).where(ProductType.id == product.product_type_id)))
                .scalars()
                .one()
            )
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=PRODUCT_INFO_MESSAGE_TEMPLATE.format(
                    name=product.name,
                    profitability=product.profitability,
                    agent_profitability=product.agent_profitability,
                    placement_period=product.placement_period,
                    product_type=product_type.name,
                ),
            )
            return ConversationHandler.END
