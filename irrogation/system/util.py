from __future__ import with_statement  # Required in 2.5
import signal
from contextlib import contextmanager


class TimeoutException(Exception):
    pass


@contextmanager
def time_limit(seconds, finalmethod):
    def signal_handler(signum, frame):
        raise TimeoutException

    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)
        finalmethod()


def printstate(balkony_entities):
    message = ""
    for i in balkony_entities:
        message += "Kasten {}, akt. Hum. {}%, Ziel {}".format(i.no, i.get_humidity() * 100, i.target_humidity) + "\n"
    print message
    return message

# def test():
#     register_entities()
#     from irrogation.system.raspberry import mcp
#     while True:
#         mcp.power_on()
#         for i in balkony_entities:
#             print "{0}: {1: >5} | ".format(i.no, i.get_true_humidity()),
#         print
#         mcp.power_off()
#         time.sleep(5)