from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup


def show_table_actions_kb(table_name):
    kb = InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton(text='Добавить', callback_data=f'table_add_{table_name}'),
        InlineKeyboardButton(text='Получить', callback_data=f'table_get_{table_name}'),
    )
    return kb


def get_categories(categories):
    kb = InlineKeyboardMarkup(row_width=2)
    buttons = []
    for category in categories:
        buttons.append(
            InlineKeyboardButton(text=category.name, callback_data=f'get_category:{category.id}')
        )
    kb.add(*buttons)
    return kb


def show_table_item_actions_kb(item_name: str, item_id: int):
    """

    :param table_name:
    :param item_id:
    :return:
    """
    kb = InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton(text='Удалить', callback_data=f'delete_{item_name}:{item_id}'),
        InlineKeyboardButton(text='Добавить', callback_data=f'update_{item_name}:{item_id}'),
    )
    return kb