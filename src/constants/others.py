import re
from typing import Final

from telegram.constants import ChatMemberStatus

MISSING_VALUE: Final[str] = "Отсутствует"
SUPPORT_DIALOG_ID_PATTERN = re.compile(r"№(\d+)", re.IGNORECASE | re.MULTILINE)

NOT_CHANEL_USER_STATUSES: Final[frozenset[ChatMemberStatus]] = frozenset(
    {ChatMemberStatus.LEFT, ChatMemberStatus.RESTRICTED, ChatMemberStatus.BANNED}
)
