# Lora Receiver Code for Raspberry Pi: (Download the required libraries from here)

from time import sleep
from SX127x.LoRa import *
from SX127x.board_config import BOARD
import requests
import json
from datetime import datetime
import pygsheets

#authorization
gc = pygsheets.authorize(service_file='/home/pi/workspace/arduino-monitoring/PiServer/GoogleDriveCreds.json')

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

def escapeString(input):
    escapes = ''.join([chr(char) for char in range(0, 32)])
    translator = str.maketrans('', '', escapes)
    return input.translate(translator)

class LoRaRcvCont(LoRa):
    def __init__(self, verbose=False):
        super(LoRaRcvCont, self).__init__(verbose)
        self.set_mode(MODE.SLEEP)
        self.set_dio_mapping([0] * 6)

    def start(self):
        self.reset_ptr_rx()
        self.set_mode(MODE.RXCONT)
        while True:
            sleep(.5)
            sys.stdout.flush()

    def on_payload_crc_error(self):
        now = datetime.now()
        time = now.strftime("%m/%d/%Y %H:%M:%S")
        irqFlags = self.get_irq_flags()
        wks.append_table(values=[time, "CRC Error encountered", irqFlags])
        print("\nPayload error")
        print("\non_PayloadCrcError")
        print(irqFlags)

    def on_rx_done(self):
        now = datetime.now()
        time = now.strftime("%m/%d/%Y %H:%M:%S")
        print("\nTime: ")
        print(time)

        try:
            self.clear_irq_flags(RxDone=1)
            payload = ((bytes)(self.read_payload(nocheck=True))).decode("utf-8", 'ignore')

            payload = escapeString(payload)

            rsi = self.get_rssi_value()
            print("\nRSSI: ")
            print(rsi)
            print("\nReceived: ")
            print(repr(payload))

            wks.append_table(values=[time, rsi, payload])

            self.set_mode(MODE.SLEEP)
            self.reset_ptr_rx()
            self.set_mode(MODE.RXCONT)

            payloadObject = json.loads(payload)
            requestPayload = ""

            for key in payloadObject:
                if key in propertyToField:
                    requestPayload += f'{propertyToField[key]}={payloadObject[key]}&'

            if len(requestPayload) > 0:
                # post data to dashboard
                request = f'https://api.thingspeak.com/update?api_key={thingsSpeakWriteKey}&{requestPayload}'
                print(request)
                response = requests.get(request)
                print(response)
            else:
                print("Failed to decode message.")
        except BaseException as err:
            message = "Receive error: {0}".format(err)
            print(message)
            wks.append_table(values=[time, message])



lora = LoRaRcvCont(verbose=True)
lora.set_mode(MODE.STDBY)

#  Medium Range  Defaults after init are 434.0MHz, Bw = 125 kHz, Cr = 4/5, Sf = 128chips/symbol, CRC on 13 dBm
lora.set_pa_config(pa_select=1)
lora.set_spreading_factor(10)
lora.set_rx_crc(True)

try:
    print("started")
    lora.start()
except KeyboardInterrupt:
    sys.stdout.flush()
    print("")
    sys.stderr.write("KeyboardInterrupt\n")
except BaseException as err:
    message = "Application error: {0}".format(err)
    print(message)
    wks.append_table(values=[message])
finally:
    sys.stdout.flush()
    print("")
    lora.set_mode(MODE.SLEEP)
    BOARD.teardown()
