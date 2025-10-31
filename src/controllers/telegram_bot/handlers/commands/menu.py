from dependency_injector.wiring import Provide, inject
from loguru import logger
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from src.constants import MENU_COMMAND_MESSAGE, PROGRAM_TYPE_CALLBACK_TEMPLATE
from src.container import AppContainer
from src.controllers.telegram_bot.states import START_ROUTES
from src.gateways.database.models import Product, ProductType


@inject
async def get_menu(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,  # noqa: ARG001
    session: async_sessionmaker = Provide[AppContainer.session_maker],
) -> int:
    logger.info("Запущена команда /menu")
    async with session() as _session:
        product_types_with_products = (
            (
                await _session.execute(
                    select(ProductType).join(Product, ProductType.id == Product.product_type_id).distinct()
                )
            )
            .scalars()
            .all()
        )
        await update.message.reply_text(
            MENU_COMMAND_MESSAGE,
            reply_markup=InlineKeyboardMarkup(
                [
                    (
                        InlineKeyboardButton(
                            product_type.name, callback_data=PROGRAM_TYPE_CALLBACK_TEMPLATE + str(product_type.id)
                        ),
                    )
                    for product_type in product_types_with_products
                ]
            ),
        )
    return START_ROUTES
