import telegram
from . import config
from irrogation import system

print telegram

irrogationbot = telegram.Bot(token=config.TELEGRAM_TOKEN)


def start():
    for u in config.USERS:
        irrogationbot.send_message(u.userid, config.WELCOME_MESSAGE.format(u.name))
        irrogationbot.send_message(u.userid, system.printstate())

