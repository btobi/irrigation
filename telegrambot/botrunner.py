# coding=utf-8
import atexit

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.error import Unauthorized, BadRequest, TimedOut, NetworkError, ChatMigrated, TelegramError
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

from irrogation.system.system import exit_functions
from telegrambot import config
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

updater = Updater(config.TELEGRAM_TOKEN)
dispatcher = updater.dispatcher


def send_message(message):
    for user in config.USERS:
        updater.bot.send_message(chat_id=user.userid, text=message)


def water(bot, update, args):
    update.message.reply_text('Balkonkasten wählen:', reply_markup=get_entity_buttons())


def water_callback(bot, update):
    query = update.callback_query

    if query.data == "cancel":
        bot.edit_message_text(text="canceled",
                              chat_id=query.message.chat_id,
                              message_id=query.message.message_id)
        return

    bot.edit_message_text(text="Auswahl Balkonkasten: %s" % query.data,
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id)

    bot.send_message(chat_id=query.message.chat_id, text="Wasser start.")

    entity_id = query.data

    from irrogation.system.system_entities import balkony_entities
    filter(lambda x: x.no == int(entity_id), balkony_entities)[0].waterforce()

    bot.send_message(chat_id=query.message.chat_id, text="Wasser ende.")


def status(bot, update, args):
    update.message.reply_text("Current status:")
    from irrogation.system import system
    update.message.reply_text(system.get_humidity_message())


def error_callback(bot, update, error):
    try:
        raise error
    except Unauthorized:
        bot.send_message(chat_id=update.message.chat_id, text="Unauthorized")
    except BadRequest:
        bot.send_message(chat_id=update.message.chat_id, text="Bad request")
    except TimedOut:
        bot.send_message(chat_id=update.message.chat_id, text="Timeout")
    except NetworkError:
        bot.send_message(chat_id=update.message.chat_id, text="Network error")
    except ChatMigrated as e:
        bot.send_message(chat_id=update.message.chat_id, text="Chat has migrated")
    except TelegramError:
        bot.send_message(chat_id=update.message.chat_id, text="Telegram Error")


def run_bot():
    dispatcher.add_handler(CommandHandler('water', water, pass_args=True))
    dispatcher.add_handler(CommandHandler('status', status, pass_args=True))
    dispatcher.add_handler(CallbackQueryHandler(water_callback))
    dispatcher.add_error_handler(error_callback)

    welcome_message = "BOT STARTED \n"
    welcome_message += "/water \n"
    welcome_message += "/status \n"

    updater.bot.send_message(chat_id=config.USERS[0].userid, text=welcome_message)

    updater.start_polling()
    updater.idle()


def get_entity_buttons():
    from irrogation.system.system_entities import balkony_entities
    button_list = [InlineKeyboardButton(text="Nr: {}".format(i.no), callback_data=str(i.no)) for i in
                   balkony_entities]
    footer_button = InlineKeyboardButton(text="Cancel", callback_data="cancel")
    return InlineKeyboardMarkup(build_menu(button_list, n_cols=2, footer_buttons=[footer_button]))
    # return InlineKeyboardMarkup(build_menu(button_list, n_cols=2))


def build_menu(buttons, n_cols, header_buttons=None, footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu


class DummyEntity(object):
    def __init__(self, no):
        self.no = no


if __name__ == '__main__':
    run_bot()

atexit.register(exit_functions)
