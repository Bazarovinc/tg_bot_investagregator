import asyncio

from dependency_injector.wiring import Provide, inject
from loguru import logger
from sqlalchemy.ext.asyncio import async_sessionmaker
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from src.constants import (
    PRODUCT_TYPE_SAVED_MESSAGE_TEMPLATE,
)
from src.container import AppContainer
from src.gateways.database.models import ProductType


@inject
async def add_new_product_type(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    session: async_sessionmaker = Provide[AppContainer.session_maker],
) -> int:
    logger.info("Добавлено имя новой группы продуктов")
    product_type_name = update.message.text
    print(product_type_name)
    async with session() as _session:
        _session.add(ProductType(name=product_type_name))
        await asyncio.gather(
            *(
                _session.commit(),
                context.bot.send_message(
                    text=PRODUCT_TYPE_SAVED_MESSAGE_TEMPLATE.format(product_type_name=product_type_name),
                    chat_id=update.effective_chat.id,
                ),
            )
        )
    return ConversationHandler.END
