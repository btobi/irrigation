import atexit
import thread
import time

from irrogation.system import scheduler
from system_entities import balkony_entities


def run():
    from irrogation.system.raspberry import mcp
    mcp.power_off()
    send_welcome_message()
    for i in balkony_entities:
        i.pump.off()
    # thread.start_new_thread(forced_irrogation, ())
    # thread.start_new_thread(irrogation, ())
    # thread.start_new_thread(observation, ())
    observation()


def send_welcome_message():
    from telegrambot import botrunner
    message = "Irrogation system has started \n"
    message += get_humidity_message()
    # print message
    botrunner.send_message(message)


def get_humidity_message():
    message = ""
    from irrogation.system.raspberry import mcp
    mcp.power_on()
    message += "\n".join(
        ["Entity {}: {}% (hum)".format(str(entity.no), str(entity.get_humidity() * 100)) for entity in
         balkony_entities])
    for entity in balkony_entities:
        entity.log()
    mcp.power_off()
    return message


def forced_irrogation():
    print "entering forced irrogation"
    scheduler.run_hourly((lambda: i.waterforce() for i in balkony_entities))


def irrogation():
    scheduler.run_hourly((lambda: i.water() for i in balkony_entities))


def observation():
    def log_all():
        from irrogation.system.raspberry import mcp
        mcp.power_on()
        for i in balkony_entities:
            i.log()
        mcp.power_off()
    scheduler.run_hourly(log_all)


def exit_functions():
    print "Closing SPI-DEV interface. Shutting down sensors."
    from irrogation.system.raspberry import mcp
    mcp.close()

    print "Shutting down pumps."
    for b in balkony_entities:
        b.pump.off()


atexit.register(exit_functions)
