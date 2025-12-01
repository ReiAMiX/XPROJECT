from apps.tg_bot.data.loader import bot
from telebot import types
from apps.tg_bot.keyboards.inline import get_categories, show_table_item_actions_kb, show_table_actions_kb
from apps.main.models import Category
from apps.tg_bot.utils import is_admin



def get_message_and_chat_id(call: types.CallbackQuery) -> tuple:
    return call.message.chat.id, call.message.message_id


@bot.message_handler(
    func=lambda msg: msg.text == "Категории" and is_admin
)
def handle_admin_categories(message: types.Message):
    bot.reply_to(message, "Выберите действие над категориями",
                 reply_markup=show_table_actions_kb('categories'))


@bot.callback_query_handler(
    func=lambda call: call.data == 'table_get_categories' and is_admin
)
def handle_categories_get(call: types.CallbackQuery):
    chat_id, message_id = get_message_and_chat_id(call)

    categories = Category.objects.all()
    bot.edit_message_text(
        chat_id=chat_id,
        message_id=message_id,
        text='Выберите категорию',
        reply_markup=get_categories(categories)
    )


@bot.callback_query_handler(
    func=lambda call: call.data.startswith("get_category") and is_admin
)
def handle_categories_actions(call: types.CallbackQuery):
    chat_id = call.message.chat.id
    message_id = call.message.message_id

    category_id = call.data.split(":")[-1]
    category_object = Category.objects.get(id=category_id)

    bot.edit_message_text(
        chat_id=chat_id,
        message_id=message_id,
        text=f"Выберите действие ниже для категории: <b>{category_object.name}</b>",
        reply_markup=show_table_item_actions_kb("category", category_object.id)
    )


@bot.callback_query_handler(
    func=lambda call: call.data.startswith("delete_category") and is_admin
)
def handle_categories_delete(call: types.CallbackQuery):
    category_id = call.data.split(":")[-1]

    chat_id, message_id = get_message_and_chat_id(call)

    category = Category.objects.get(id=category_id)

    bot.edit_message_text(
        chat_id=chat_id,
        message_id=message_id,
        text=f"Вы действительно хотите удалить категорию: <b>{category.name}</b>",
    )

@bot.callback_query_handler(
    func=lambda call: call.data.startswith("update_category") and is_admin
)
def handle_update_category(call: types.CallbackQuery):
    chat_id, message_id = get_message_and_chat_id(call)
    bot.edit_message_text(
        chat_id=chat_id,
        message_id=message_id,
        text="Напиши новое название категории"
    )