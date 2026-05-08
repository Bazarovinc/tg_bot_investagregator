from loguru import logger
from telegram import ChatFullInfo, Update
from telegram.ext import ContextTypes, ConversationHandler

from src.controllers.telegram_bot.utils.admin_virfication import verify_chat_id
from src.settings.app import app_settings


@verify_chat_id(app_settings.telegram.master_id)
async def get_chat_id_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,  # noqa: ARG001
) -> int:
    logger.info("Запущена команда /chat_id")
    chat_info: ChatFullInfo = await context.bot.get_chat(app_settings.telegram.guard_chanel_id)
    await update.message.reply_text(str(chat_info.id))
    return ConversationHandler.END

    await self.uow.phys_data_in_repo.update(  # type: ignore
        {
            "confirm_type": parsed_message.confirm_type,
            "checked_flg": CheckedFlagEnum.checked.value,
            "last_upd_by": self.pod_name
        },
        UpdateFilterSet(
            {
                "last_nm": EqualFilter(parsed_message.last_nm, eq=True),
                "doc_series": EqualFilter(parsed_message.doc_series, eq=True),
                "doc_num": EqualFilter(parsed_message.doc_num, eq=True),
                "sim_flg": EqualFilter(SimFlagEnum.FINAL_BLOCK.value, neq=True),
                "confirm_type": SingleFieldOrFilter(
                    (EqualFilter(None, eq=True),
                     EqualFilter(IdentificationTypeEnum.OTHER.value, eq=True),
                     EqualFilter(IdentificationTypeEnum.PASSPORT_RF.value, eq=True),
                     EqualFilter(IdentificationTypeEnum.UKEP.value, eq=True),
                     )),
                "confirm_type": EqualFilter(parsed_message.confirm_type, neq=True),
                "msisdn": SequenceFilter(parsed_message.msisdn_list, in_=True)

            }
        )
    )