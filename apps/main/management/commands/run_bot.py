from django.core.management import BaseCommand
from apps.tg_bot.data.loader import bot
from apps.tg_bot.handlers import admin
from apps.tg_bot.handlers import user


class Command(BaseCommand):
    def handle(self, *args, **options):
        print('bot_started')
        bot.polling(non_stop=True)
        print('bot_stopped')