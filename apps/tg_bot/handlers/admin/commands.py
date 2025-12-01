from telebot import types

from apps.tg_bot.data.loader import bot
from apps.tg_bot.keyboards.reply import show_admin_start_kb
from apps.tg_bot.utils import is_admin

@bot.message_handler(commands=['start'], func=is_admin)
def handle_admin_start(message: types.Message):
    bot.reply_to(message, "Вы Администратор", reply_markup=show_admin_start_kb())


@bot.message_handler(
    func=lambda message: message.text == "Комментарии" and is_admin
)

def handle_admin_comments(message: types.Message):
    bot.reply_to(message, "Все Комментарии")

@bot.message_handler(
    func=lambda message: message.text == "Посты" and is_admin
)

def handle_admin_posts(message: types.Message):
    bot.reply_to(message, "Все Посты")

@bot.message_handler(
    func=lambda message: message.text == "Пользователи" and is_admin
)

def handle_admin_users(message: types.Message):
    bot.reply_to(message, "Все Пользователи")

