from irrogation import irrogation_system
# from irrogation import raspberry
import logging
import time

# from telegrambot import botrunner
from telegrambot import botrunner

print "starting irrogation bot"

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

botrunner.run_bot()
