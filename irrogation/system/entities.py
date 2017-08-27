import time

from sqlalchemy import desc

from database.models import session, SensorLog
from irrogation import config
from irrogation.system import raspberry


class BalkonyEntity(object):
    def __init__(self, no, pump, humidity_sensor, target_humidity):
        self.pump = pump
        self.humidity_sensor = humidity_sensor
        self.target_humidity = target_humidity
        self.no = no

    def __toodry__(self):
        print "Check if Entity {} is too dry. Current: {}, Expected: {}".format(self.no,
                                                                                self.humidity_sensor.getvalue(),
                                                                                self.target_humidity)
        return self.humidity_sensor.getvalue() < self.target_humidity

    def water(self):
        print "Start watercheck for {}".format(self.no)
        if True and self.__toodry__():
            print "Entity {} is too dry. Start watering...".format(self.no)
            # with util.time_limit(360, self.pump.off):
            self.pump.on()
            t = 0
            while self.__toodry__() and t < 5:
                time.sleep(5)
                t += 1
            self.pump.off()

    def waterforce(self):
        from telegrambot import botrunner
        botrunner.send_message("Water entitiy {} start.".format(self.no))
        self.pump.on()
        time.sleep(60)
        self.pump.off()
        botrunner.send_message("Water entitiy {} stop.".format(self.no))

    def get_humidity(self):
        last_entries = session.query(SensorLog).filter(SensorLog.type == "HUMIDITY").filter(
            SensorLog.entity_id == self.no).order_by(desc(SensorLog.date)).limit(3).all()
        data = map(lambda e: e.data, last_entries)
        data.append(self.humidity_sensor.getvalue())
        new_value = round(reduce(lambda x, y: x + y, data, 0) / len(data), 3)
        return new_value

    def get_true_humidity(self):
        return self.humidity_sensor.gettruevalue()

    def log(self):
        print "Logging Entity {}".format(self.no)
        log = SensorLog(self.no, "HUMIDITY", self.get_humidity())
        session.add(log)
        session.commit()


class Pump(object):
    def __init__(self, pin_number):
        self.pin = raspberry.Pin(pin_number)

    def on(self):
        self.pin.on()

    def off(self):
        self.pin.off()


class HumiditySensor(object):
    def __init__(self, pin_number):
        self.pin_number = pin_number

    def getvalue(self):
        return self.__normalizevalue__(raspberry.mcp.read(self.pin_number))

    def gettruevalue(self):
        return raspberry.mcp.read(self.pin_number)

    @staticmethod
    def __normalizevalue__(value):
        # if value > config.HUMIDITY_VALUE_HIGH or value < config.HUMIDITY_VALUE_LOW:
        #  return "invalid"
        return 1.0 - (float(value) - config.HUMIDITY_VALUE_LOW) / (
            config.HUMIDITY_VALUE_HIGH - config.HUMIDITY_VALUE_LOW)
