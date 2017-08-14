import atexit
import thread

import time

from irrogation import scheduler
from irrogation.entities import BalkonyEntity, Pump, HumiditySensor

balkony_entities = []


def register_entities():
    balkony_entities.append(BalkonyEntity(0, Pump(31), HumiditySensor(0), 0.7))
    balkony_entities.append(BalkonyEntity(1, Pump(33), HumiditySensor(1), 0.7))
    balkony_entities.append(BalkonyEntity(2, Pump(40), HumiditySensor(2), 0.7))
    balkony_entities.append(BalkonyEntity(3, Pump(33), HumiditySensor(3), 0.7))
    balkony_entities.append(BalkonyEntity(4, Pump(35), HumiditySensor(4), 0.7))


def run():
    print "Running Irrogation System. Registering Balkony Entities..."
    register_entities()

    print "Humidity Status:"
    for i in balkony_entities:
        print "Entity {}, Humidity {} ({}), Target {}".format(i.no, i.get_humidity(), i.get_true_humidity(), i.target_humidity)

    # thread.start_new_thread(irrogation, ())
    thread.start_new_thread(observation, ())

    #balkony_entities[2].waterforce()


def irrogation():
    scheduler.run_hourly(check_and_run)


def check_and_run():
    for i in balkony_entities:
        i.water()


def printstate():
    message = ""
    for i in balkony_entities:
        message += "Kasten {}, akt. Hum. {}%, Ziel {}".format(i.no, i.get_humidity() * 100, i.target_humidity) + "\n"
    print message
    return message


def observation():
    scheduler.run_minutely(log_all)


def log_all():
    for i in balkony_entities:
        i.log()


def test():
    register_entities()
    from irrogation.raspberry import mcp
    while True:
        mcp.power_on()
        for i in balkony_entities:
            print "{0}: {1: >5} | ".format(i.no, i.get_true_humidity()),
        print
        mcp.power_off()
        time.sleep(5)


def exit_functions():
    print "Closing SPI-DEV interface. Shutting down sensors."
    from irrogation.raspberry import mcp
    mcp.close()

    print "Shutting down pumps."
    for b in balkony_entities:
        b.pump.off()

atexit.register(exit_functions)
