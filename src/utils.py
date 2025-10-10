import re


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
