from irrogation import system
# from irrogation import raspberry
import logging
import time

# from telegrambot import botrunner

print "starting irrogation control app"

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

system.run()
#botrunner.start()

while True:
    print "hello"
    time.sleep(1)




# raspberry.GPIO.cleanup()
