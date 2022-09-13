from SX127x.LoRa import *
from SX127x.board_config import BOARD
from SX127x.constants import *
import json
import pygsheets
from LoraReceiver import LoraReceiver
from StreamToLogger import StreamToLogger
import sys
import logging
import logging_loki

handler = logging_loki.LokiHandler(
    url="http://localhost:3100/loki/api/v1/push",
    tags={"application": "lora-receiver"},
    auth=("admin", "admin"),
    version="1",
)

logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')

logger = logging.getLogger('logger')

logger.addHandler(handler)

sys.stdout = StreamToLogger(logger,logging.INFO)
sys.stderr = StreamToLogger(logger,logging.ERROR)

#authorization
gc = pygsheets.authorize(service_file='/home/pi/workspace/arduino-monitoring/PiServer/environment.json')

#open the google spreadsheet
sh = gc.open('Arduino Monitoring')
wks = sh[0]

environmentVariables = open('/home/pi/workspace/arduino-monitoring/PiServer/environment.json', "r")

environmentVariablesJson = json.loads(environmentVariables.read())

thingsSpeakWriteKey = environmentVariablesJson["ts_write_key"]
thingsSpeakReadKey = environmentVariablesJson["ts_read_key"]

environmentVariables.close()

propertyToField = {
    "psc": "field1",
    "hmd": "field2",
    "tmp": "field3",
    "lux": "field4"
}

data = 1

BOARD.setup()
BOARD.reset()

lora = LoraReceiver(verbose=True, wks=wks, propertyToField=propertyToField, thingsSpeakWriteKey=thingsSpeakWriteKey)
lora.set_mode(MODE.STDBY)

#  Medium Range  Defaults after init are 434.0MHz, Bw = 125 kHz, Cr = 4/5, Sf = 128chips/symbol, CRC on 13 dBm
lora.set_pa_config(pa_select=1)
lora.set_spreading_factor(10)
lora.set_rx_crc(True)
lora.set_bw(BW.BW62_5)

try:
    print("started")
    lora.start()
except KeyboardInterrupt:
    sys.stdout.flush()
    sys.stderr.write("KeyboardInterrupt\n")
except BaseException as err:
    message = "Application error: {0}".format(err)
    print(message)
    wks.append_table(values=[message])
finally:
    sys.stdout.flush()
    lora.set_mode(MODE.SLEEP)
    BOARD.teardown()
