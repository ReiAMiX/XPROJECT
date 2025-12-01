from apps.tg_bot.data.loader import bot
from apps.tg_bot.keyboards.reply import start_kb


@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(
        chat_id=message.chat.id,
        text='Привет',
        reply_markup=start_kb()
    )


@bot.message_handler(function=lambda message: message.text == 'Запуск')
def handle_start(message):
    bot.reply_to(message, message.text)