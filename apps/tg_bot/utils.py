from django.conf import settings
from telebot import types


def is_admin(obj):
    if isinstance(obj, types.Message):
        return obj.chat.id == int(settings.MAIN_CHAT_ID)

    return obj.chat.id == int(settings.MAIN_CHAT_ID)