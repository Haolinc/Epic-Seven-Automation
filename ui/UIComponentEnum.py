from enum import Enum


class LabelEnum(Enum):
    COVENANT_COUNT = 'covenant_count_label'
    MYSTIC_COUNT = 'mystic_count_label'
    TOP = 'top_label'
    ARENA = 'arena_label'


class ButtonEnum(Enum):
    SHOP_REFRESH_START = 'start_shop_refresh_button'
    ARENA_START = 'start_arena_button'


class EntryEnum(Enum):
    SHOP_REFRESH_COUNT_ENTRY = 'refresh_shop_count_entry'
    ARENA_COUNT_ENTRY = 'arena_count'


class UIComponent(Enum):
    SHOP_REFRESH = "SHOP"
    ARENA = "ARENA"
