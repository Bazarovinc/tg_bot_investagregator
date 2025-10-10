from telegram import BotCommand
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ConversationHandler, MessageHandler, filters

from src.constants import (
    ADMIN_CALLBACK_TEMPLATE,
    ADMIN_COMMAND_NAME,
    CANCEL_CALLBACK_TEMPLATE,
    HELP_COMMAND_INFO,
    HELP_COMMAND_NAME,
    MENU_COMMAND_INFO,
    MENU_COMMAND_NAME,
    PRODUCT_ACTION_CALLBACK_TEMPLATE,
    PRODUCT_CALLBACK_TEMPLATE,
    PRODUCT_FOR_EDIT_CALLBACK_TEMPLATE,
    PRODUCT_TYPE_FOR_PRODUCT_EDIT_CALLBACK_TEMPLATE,
    PROGRAM_TYPE_CALLBACK_TEMPLATE,
    START_COMMAND_INFO,
    START_COMMAND_NAME,
)
from src.constants.templates import (
    PRODUCT_TYPE_FOR_NEW_PRODUCT_CALLBACK_TEMPLATE,
)
from src.controllers.telegram_bot.handlers import (
    add_new_product_type,
    add_product_agent_profitability_and_send_next_question,
    add_product_description_and_send_next_question,
    add_product_file_and_save_product,
    add_product_name_and_send_next_question,
    add_product_placement_period_state_and_send_next_question,
    add_product_profitability_and_send_next_question,
    edit_file_path,
    edit_product_agent_profitability,
    edit_product_description,
    edit_product_name,
    edit_product_placement_period,
    edit_product_profitability,
    edit_product_type_name,
    get_action_callback,
    get_admin_callback,
    get_admin_message,
    get_cancel_callback,
    get_finish_callback,
    get_help_message,
    get_menu,
    get_menu_callback,
    get_ordering_callback,
    get_product_callback_and_send_action_selection,
    get_product_description_skipp_callback,
    get_product_type_action_callback,
    get_product_type_for_next_action_callback,
    get_product_type_for_product_selection_callback,
    get_product_type_id_callback_and_send_next_question,
    get_start_message,
)
from src.controllers.telegram_bot.handlers.callbacks import get_product_callback
from src.controllers.telegram_bot.states import (
    ADD_NEW_PRODUCT_TYPE_STATE,
    ADD_PRODUCT_AGENT_PROFITABILITY_STATE,
    ADD_PRODUCT_DESCRIPTION_STATE,
    ADD_PRODUCT_FILE_STATE,
    ADD_PRODUCT_NAME_STATE,
    ADD_PRODUCT_PLACEMENT_PERIOD_STATE,
    ADD_PRODUCT_PROFITABILITY_STATE,
    ADD_PRODUCT_TYPE_STATE,
    ADMIN_START_STATE,
    EDIT_PRODUCT_AGENT_PROFITABILITY_STATE,
    EDIT_PRODUCT_DESCRIPTION_STATE,
    EDIT_PRODUCT_FILE_PATH_STATE,
    EDIT_PRODUCT_NAME_STATE,
    EDIT_PRODUCT_PLACEMENT_PERIOD_STATE,
    EDIT_PRODUCT_PROFITABILITY_STATE,
    EDIT_PRODUCT_TYPE_NAME_STATE,
    SELECT_PRODUCT_ACTION_STATE,
    SELECT_PRODUCT_FOR_EDIT_STATE,
    SELECT_PRODUCT_TYPE_ACTION_STATE,
    SELECT_PRODUCT_TYPE_FOR_EDIT_PRODUCT_STATE,
    SELECT_PRODUCT_TYPE_FOR_EDIT_STATE,
)

START_COMMAND_HANDLER = CommandHandler(
    START_COMMAND_NAME,
    get_start_message,
    filters=filters.ChatType.PRIVATE,
)
HELP_COMMAND_HANDLER = CommandHandler(
    HELP_COMMAND_NAME,
    get_help_message,
    filters=filters.ChatType.PRIVATE,
)

MENU_COMMAND_HANDLER = CommandHandler(
    MENU_COMMAND_NAME,
    get_menu,
    filters=filters.ChatType.PRIVATE,
)
ADMIN_COMMAND_HANDLER = CommandHandler(ADMIN_COMMAND_NAME, get_admin_message)  # , filters=filters.ChatType.PRIVATE)

MENU_QUERY_HANDLER = CallbackQueryHandler(
    get_menu_callback,
    pattern="^" + rf"{PROGRAM_TYPE_CALLBACK_TEMPLATE}\d+" + "$",
)
ORDER_QUERY_HANDLER = CallbackQueryHandler(get_ordering_callback, pattern="^order_")

PRODUCT_QUERY_HANDLER = CallbackQueryHandler(
    get_product_callback,
    pattern="^" + rf"{PRODUCT_CALLBACK_TEMPLATE}\d+" + "$",
)

ADMIN_QUERY_HANDLER = CallbackQueryHandler(
    get_admin_callback,
    pattern="^" + rf"{ADMIN_CALLBACK_TEMPLATE}\d+" + "$",
)

ADD_NEW_PRODUCT_TYPE_MESSAGE_HANDLER = MessageHandler(
    filters.TEXT & ~filters.COMMAND & filters.REPLY, add_new_product_type
)
ADD_NEW_PRODUCT_NAME_MESSAGE_HANDLER = MessageHandler(
    filters.TEXT & ~filters.COMMAND & filters.REPLY, add_product_name_and_send_next_question
)
ADD_NEW_PRODUCT_PRODUCT_TYPE_ID_CALLBACK_QUERY_HANDLER = CallbackQueryHandler(
    get_product_type_id_callback_and_send_next_question,
    pattern="^" + rf"{PRODUCT_TYPE_FOR_NEW_PRODUCT_CALLBACK_TEMPLATE}\d+" + "$",
)
ADD_NEW_PRODUCT_PROFITABILITY_MESSAGE_HANDLER = MessageHandler(
    filters.TEXT & ~filters.COMMAND & filters.REPLY, add_product_profitability_and_send_next_question
)
ADD_NEW_PRODUCT_AGENT_PROFITABILITY_MESSAGE_HANDLER = MessageHandler(
    filters.TEXT & ~filters.COMMAND & filters.REPLY, add_product_agent_profitability_and_send_next_question
)
ADD_NEW_PRODUCT_PLACEMENT_PERIOD_MESSAGE_HANDLER = MessageHandler(
    filters.TEXT & ~filters.COMMAND & filters.REPLY, add_product_placement_period_state_and_send_next_question
)
ADD_NEW_PRODUCT_DESCRIPTION_MESSAGE_HANDLER = MessageHandler(
    filters.TEXT & ~filters.COMMAND & filters.REPLY, add_product_description_and_send_next_question
)
SKIPP_ADD_NEW_PRODUCT_DESCRIPTION_CALLBACK_QUERY_HANDLER = CallbackQueryHandler(
    get_product_description_skipp_callback,
)
ADD_NEW_PRODUCT_FILE_MESSAGE_HANDLER = MessageHandler(
    ~filters.COMMAND & filters.REPLY, add_product_file_and_save_product
)
FINISH_ADDING_NEW_PRODUCT_CALLBACK_QUERY_HANDLER = CallbackQueryHandler(
    get_finish_callback,
)
CANCEL_ADMIN_CALLBACK_QUERY_HANDLER = CallbackQueryHandler(get_cancel_callback, pattern=CANCEL_CALLBACK_TEMPLATE)
SELECT_PRODUCT_TYPE_FOR_ADMIN_ACTION_CALLBACK_QUERY_HANDLER = CallbackQueryHandler(
    get_product_type_for_next_action_callback,
)
SELECT_PRODUCT_TYPE_ACTION_CALLBACK_QUERY_HANDLER = CallbackQueryHandler(
    get_product_type_action_callback,
)
EDIT_PRODUCT_TYPE_NAME_MESSAGE_HANDLER = MessageHandler(
    filters.TEXT & ~filters.COMMAND & filters.REPLY, edit_product_type_name
)
SELECT_PRODUCT_BY_PRODUCT_TYPE_FOR_EDIT_CALLBACK_QUERY_HANDLER = CallbackQueryHandler(
    get_product_type_for_product_selection_callback,
    pattern="^" + rf"{PRODUCT_TYPE_FOR_PRODUCT_EDIT_CALLBACK_TEMPLATE}\d+" + "$",
)

SELECT_PRODUCT_FOR_EDIT_CALLBACK_QUERY_HANDLER = CallbackQueryHandler(
    get_product_callback_and_send_action_selection,
    pattern="^" + rf"{PRODUCT_FOR_EDIT_CALLBACK_TEMPLATE}\d+" + "$",
    # pattern="^" + PRODUCT_ACTION_CALLBACK_TEMPLATE,
)

SELECT_PRODUCT_ACTION_CALLBACK_QUERY_HANDLER = CallbackQueryHandler(
    get_action_callback,
    pattern="^" + PRODUCT_ACTION_CALLBACK_TEMPLATE,
)

EDIT_PRODUCT_NAME_MESSAGE_HANDLER = MessageHandler(filters.TEXT & ~filters.COMMAND & filters.REPLY, edit_product_name)
EDIT_PRODUCT_PROFITABILITY_MESSAGE_HANDLER = MessageHandler(
    filters.TEXT & ~filters.COMMAND & filters.REPLY, edit_product_profitability
)
EDIT_PRODUCT_AGENT_PROFITABILITY_MESSAGE_HANDLER = MessageHandler(
    filters.TEXT & ~filters.COMMAND & filters.REPLY, edit_product_agent_profitability
)
EDIT_PRODUCT_PLACEMENT_PERIOD_MESSAGE_HANDLER = MessageHandler(
    filters.TEXT & ~filters.COMMAND & filters.REPLY, edit_product_placement_period
)
EDIT_PRODUCT_DESCRIPTION_MESSAGE_HANDLER = MessageHandler(
    filters.TEXT & ~filters.COMMAND & filters.REPLY, edit_product_description
)
EDIT_PRODUCT_FILE_PATH_MESSAGE_HANDLER = MessageHandler(~filters.COMMAND & filters.REPLY, edit_file_path)


def get_command_handlers() -> tuple[CommandHandler, ...]:
    return (START_COMMAND_HANDLER, HELP_COMMAND_HANDLER, MENU_COMMAND_HANDLER)


def get_conversation_handlers() -> tuple[ConversationHandler, ...]:
    return (
        ConversationHandler(
            entry_points=[ADMIN_COMMAND_HANDLER],
            states={
                ADMIN_START_STATE: [ADMIN_QUERY_HANDLER],
                ADD_NEW_PRODUCT_TYPE_STATE: [ADD_NEW_PRODUCT_TYPE_MESSAGE_HANDLER],
                ADD_PRODUCT_NAME_STATE: [ADD_NEW_PRODUCT_NAME_MESSAGE_HANDLER],
                ADD_PRODUCT_TYPE_STATE: [ADD_NEW_PRODUCT_PRODUCT_TYPE_ID_CALLBACK_QUERY_HANDLER],
                ADD_PRODUCT_PROFITABILITY_STATE: [ADD_NEW_PRODUCT_PROFITABILITY_MESSAGE_HANDLER],
                ADD_PRODUCT_AGENT_PROFITABILITY_STATE: [ADD_NEW_PRODUCT_AGENT_PROFITABILITY_MESSAGE_HANDLER],
                ADD_PRODUCT_PLACEMENT_PERIOD_STATE: [ADD_NEW_PRODUCT_PLACEMENT_PERIOD_MESSAGE_HANDLER],
                ADD_PRODUCT_DESCRIPTION_STATE: [
                    ADD_NEW_PRODUCT_DESCRIPTION_MESSAGE_HANDLER,
                    SKIPP_ADD_NEW_PRODUCT_DESCRIPTION_CALLBACK_QUERY_HANDLER,
                ],
                ADD_PRODUCT_FILE_STATE: [
                    ADD_NEW_PRODUCT_FILE_MESSAGE_HANDLER,
                    FINISH_ADDING_NEW_PRODUCT_CALLBACK_QUERY_HANDLER,
                ],
                SELECT_PRODUCT_TYPE_FOR_EDIT_PRODUCT_STATE: [
                    SELECT_PRODUCT_BY_PRODUCT_TYPE_FOR_EDIT_CALLBACK_QUERY_HANDLER
                ],
                SELECT_PRODUCT_FOR_EDIT_STATE: [SELECT_PRODUCT_FOR_EDIT_CALLBACK_QUERY_HANDLER],
                SELECT_PRODUCT_ACTION_STATE: [SELECT_PRODUCT_ACTION_CALLBACK_QUERY_HANDLER],
                EDIT_PRODUCT_TYPE_NAME_STATE: [EDIT_PRODUCT_TYPE_NAME_MESSAGE_HANDLER],
                EDIT_PRODUCT_NAME_STATE: [EDIT_PRODUCT_NAME_MESSAGE_HANDLER],
                EDIT_PRODUCT_PROFITABILITY_STATE: [EDIT_PRODUCT_PROFITABILITY_MESSAGE_HANDLER],
                EDIT_PRODUCT_AGENT_PROFITABILITY_STATE: [EDIT_PRODUCT_AGENT_PROFITABILITY_MESSAGE_HANDLER],
                EDIT_PRODUCT_PLACEMENT_PERIOD_STATE: [EDIT_PRODUCT_PLACEMENT_PERIOD_MESSAGE_HANDLER],
                EDIT_PRODUCT_DESCRIPTION_STATE: [EDIT_PRODUCT_DESCRIPTION_MESSAGE_HANDLER],
                EDIT_PRODUCT_FILE_PATH_STATE: [EDIT_PRODUCT_FILE_PATH_MESSAGE_HANDLER],
                SELECT_PRODUCT_TYPE_FOR_EDIT_STATE: [SELECT_PRODUCT_TYPE_FOR_ADMIN_ACTION_CALLBACK_QUERY_HANDLER],
                SELECT_PRODUCT_TYPE_ACTION_STATE: [SELECT_PRODUCT_TYPE_ACTION_CALLBACK_QUERY_HANDLER],
            },
            fallbacks=[CANCEL_ADMIN_CALLBACK_QUERY_HANDLER],
            per_chat=True,
            per_user=False,
        ),
    )


def get_callback_query_handlers() -> tuple[CallbackQueryHandler, ...]:
    return (
        MENU_QUERY_HANDLER,
        ORDER_QUERY_HANDLER,
        PRODUCT_QUERY_HANDLER,
        # SELECT_PRODUCT_BY_PRODUCT_TYPE_FOR_EDIT_CALLBACK_QUERY_HANDLER,
        # SELECT_PRODUCT_FOR_EDIT_CALLBACK_QUERY_HANDLER,
        # SELECT_PRODUCT_ACTION_CALLBACK_QUERY_HANDLER,
    )


def get_handlers() -> tuple[ConversationHandler | CommandHandler | MessageHandler, ...]:
    return get_command_handlers() + get_callback_query_handlers() + get_conversation_handlers()


async def setup_commands(application: Application) -> None:
    # set commands
    await application.bot.set_my_commands(
        (
            BotCommand(START_COMMAND_NAME, START_COMMAND_INFO),
            BotCommand(HELP_COMMAND_NAME, HELP_COMMAND_INFO),
            BotCommand(MENU_COMMAND_NAME, MENU_COMMAND_INFO),
        )
    )
