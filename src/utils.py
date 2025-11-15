import re
from decimal import Decimal, InvalidOperation


def camel_to_snake(camel_str: str) -> str:
    """
    Функция парсинга названия из CamelCase в snake_case

    Args:
        camel_str: входная строка

    Returns:
        выходная строка
    """
    name = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", camel_str)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", name).lower()


def convert_str_to_decimal(value: str) -> Decimal | None:
    try:
        return Decimal(value.replace(",", "."))
    except InvalidOperation:
        return None


def convert_str_to_int(value: str) -> int | None:
    if value.isdigit():
        return int(value)
    return None
