import time
from spidev import SpiDev

import RPi.GPIO as GPIO

from irrogation.system import config

GPIO.setmode(GPIO.BOARD)

class Pin(object):
    def __init__(self, pin_number):
        self.pin_number = pin_number
        GPIO.setup(pin_number, GPIO.OUT)

    def on(self):
        GPIO.output(self.pin_number, GPIO.HIGH)

    def off(self):
        GPIO.output(self.pin_number, GPIO.LOW)


class NoPowerException(Exception):
    print "MCP Sensors not powered. Reading signal not possible."
    pass


class MCP3008:
    def __init__(self, bus=0, device=0):
        self.bus, self.device = bus, device
        self.spi = SpiDev()
        self.open()
        self.power_pin = Pin(config.PIN_SENSOR_POWER)
        self.powered = False

    def power_on(self):
        self.power_pin.on()
        self.powered = True
        time.sleep(0.1)

    def power_off(self):
        self.power_pin.off()
        self.powered = False

    def open(self):
        self.spi.open(self.bus, self.device)

    def read(self, channel=0):
        if self.powered is False:
            raise NoPowerException()
        adc = self.spi.xfer2([1, (8 + channel) << 4, 0])
        data = ((adc[1] & 3) << 8) + adc[2]
        return data

    def close(self):
        self.spi.close()
        self.power_pin.off()

mcp = MCP3008()
