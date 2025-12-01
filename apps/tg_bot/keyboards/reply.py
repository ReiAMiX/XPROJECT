from telebot.types import ReplyKeyboardMarkup, KeyboardButton

def start_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton("Запуск"))
    return kb


def show_admin_start_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    kb.add(
        KeyboardButton(text='Категории'),
        KeyboardButton(text='Комментарии'),
        KeyboardButton(text='Посты'),
        KeyboardButton(text='Пользователи'),
    )
    return kb

