from time import sleep
import json
import sys
import logging
from logging_loki import LokiHandler
from logging_loki import LokiHandler
from Logging.GoogleSheetsHandler import GoogleSheetsHandler
from Logging.ThingsSpeakLogger import ThingsSpeakLogger
from Logging.ThingsSpeakHandler import ThingsSpeakHandler
from threading import Timer
from threading import Lock

from SX127x.LoRa import *
from SX127x.board_config import BOARD
from SX127x.constants import *
import LoraReceiver

lokiHandler = LokiHandler(
    url="http://localhost:3100/loki/api/v1/push",
    tags={"application": "lora-receiver"},
    auth=("admin", "admin"),
    version="1")

googleSheetsHandler = GoogleSheetsHandler(
    '/home/pi/workspace/arduino-monitoring/PiServer/environment.json',
    'Arduino Monitoring')

logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')
# logging.StreamHandler()

logger = logging.getLogger('logger')
# logger.addHandler(lokiHandler)
# logger.addHandler(googleSheetsHandler)

dataLogger = logging.getLogger('data-logger')

with open('/home/pi/workspace/arduino-monitoring/PiServer/environment.json', "r") as environmentVariables:
    environmentVariablesJson = json.loads(environmentVariables.read())
    environmentVariables.close()
    thingsSpeakWriteKey = environmentVariablesJson["ts_write_key"]
    thingsSpeakHandler = ThingsSpeakHandler(logger, thingsSpeakWriteKey)
    thingsSpeakHandler.setLevel(logging.DEBUG)
    thingsSpeakHandler.setFormatter(logging.Formatter('%(message)s'))
    dataLogger.addHandler(thingsSpeakHandler)

lora = None
loraLock = Lock()

def keep_lora_alive():
    global lora
    global loraLock
    logger.info("keeping Lora receiver alive")
    if (not lora.has_received_successfully_in_last(10)):
        logger.info("shutting down Lora receiver")
        lora.dispose()
        loraLock.release()
        keepAliveTimer = Timer(10*60, keep_lora_alive)
        keepAliveTimer.start()

logger.info("started")
keepAliveTimer = Timer(10*60, keep_lora_alive)
keepAliveTimer.start()

try:
    while True:
        if lora == None or lora.disposed:
            loraLock.acquire()
            logger.info("starting new Lora receiver")
            lora = LoraReceiver.LoraReceiver(verbose=True, logger=logger, dataLogger=dataLogger)
            lora.start()
        sleep(.5)
        sys.stdout.flush()
except KeyboardInterrupt:
    sys.stdout.flush()
    sys.stderr.write("KeyboardInterrupt\n")
except BaseException as err:
    logger.exception(err)
finally:
    sys.stdout.flush()
    keepAliveTimer.cancel()
    logger.info("shutting down Lora receiver")
    lora.dispose()
