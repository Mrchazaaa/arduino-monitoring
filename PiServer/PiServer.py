from SX127x.LoRa import *
from SX127x.board_config import BOARD
from SX127x.constants import *
import json
from LoraReceiver import LoraReceiver
from Logging.StdOutLogger import StdOutLogger
import sys
import logging
from logging_loki import LokiHandler
from Logging.GoogleSheetsHandler import GoogleSheetsHandler
from Logging.ThingsSpeakLogger import ThingsSpeakLogger
from threading import Timer

logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s:%(levelname)s:%(name)s:%(message)s',
        handlers=[
            LokiHandler(
                url="http://localhost:3100/loki/api/v1/push",
                tags={"application": "lora-receiver"},
                auth=("admin", "admin"),
                version="1"),
            GoogleSheetsHandler(
                '/home/pi/workspace/arduino-monitoring/PiServer/environment.json',
                'Arduino Monitoring'),
            logging.StreamHandler()
        ])

logger = logging.getLogger('logger')

dataLogger = None
with open('/home/pi/workspace/arduino-monitoring/PiServer/environment.json', "r") as environmentVariables:
    environmentVariablesJson = json.loads(environmentVariables.read())
    environmentVariables.close()
    thingsSpeakWriteKey = environmentVariablesJson["ts_write_key"]
    dataLogger = ThingsSpeakLogger(logger, thingsSpeakWriteKey)

lora = None

def KeepLoraAlive():
    global lora
    logger.info("keeping Lora receiver alive")
    if not lora.HasReceivedSuccessfullyInLast25Mins():
        shutdownLoraReceiver()
        keepAliveTimer = Timer(25*60, KeepLoraAlive)
        keepAliveTimer.start()
        lora = startNewLoraReceiver()

def startNewLoraReceiver():
    global lora
    logger.info("started new Lora receiver")
    BOARD.setup()
    BOARD.reset()
    lora = LoraReceiver(verbose=True, logger=logger, dataLogger=dataLogger)
    lora.set_mode(MODE.STDBY)

    #  Medium Range  Defaults after init are 434.0MHz, Bw = 125 kHz, Cr = 4/5, Sf = 128chips/symbol, CRC on 13 dBm
    lora.set_pa_config(pa_select=1)
    lora.set_spreading_factor(10)
    lora.set_rx_crc(True)
    lora.set_bw(BW.BW62_5)
    lora.start()

def shutdownLoraReceiver():
    global lora
    logger.info("shutting down Lora receiver")
    lora.dispose()
    lora.set_mode(MODE.SLEEP)
    BOARD.teardown()
    lora = None

with StdOutLogger(logger, "INFO") as redirector:
    try:
        logger.info("started")
        keepAliveTimer = Timer(25*60, KeepLoraAlive)
        keepAliveTimer.start()
        startNewLoraReceiver()
    except KeyboardInterrupt:
        sys.stdout.flush()
        sys.stderr.write("KeyboardInterrupt\n")
    except BaseException as err:
        logger.exception(err)
    finally:
        sys.stdout.flush()
        shutdownLoraReceiver()
        keepAliveTimer.cancel()
