import shutil

shutil.copyfile('/settings/settings.py', './settings.py')

import telebot
from telegram.constants import ParseMode

from message_handlers import MessageHandler
import settings
from validators import UserValidator
from db_handler_selector import DbHandlerSelector

bot = telebot.TeleBot(settings.token)


@bot.message_handler()
def user_input(message):
    if not UserValidator.validate_user(message.text, message.from_user.id):
        bot.send_message(message.chat.id, 'Access denied, enter password')
        return
    response = MessageHandler.handle_message(message)
    for chat in response.chats:
        bot.send_message(chat, response.message)


if __name__ == '__main__':
    bot.parse_mode = ParseMode.HTML
    db_handler = DbHandlerSelector.get_db_handler()
    db_handler.init_db()
    bot.infinity_polling()
