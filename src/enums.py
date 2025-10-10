from enum import IntEnum


class AdminActionEnum(IntEnum):
    add_product_type = 0
    add_product = 1
    edit_product_type = 2
    edit_product = 3


class ProductTypeActionEnum(IntEnum):
    edit_name = 0
    delete_product_type = 1


class ProductActionEnum(IntEnum):
    edit_name = 0
    edit_profitability = 1
    edit_agent_profitability = 2
    edit_placement_period = 3
    edit_description = 4
    edit_file_path = 5
    delete_product = 6
