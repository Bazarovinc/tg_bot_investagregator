import re
from typing import Final

MISSING_VALUE: Final[str] = "Отсутствует"
SUPPORT_DIALOG_ID_PATTERN = re.compile(r"№(\d+)", re.IGNORECASE | re.MULTILINE)
