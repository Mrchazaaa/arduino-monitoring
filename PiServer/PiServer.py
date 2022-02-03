# Lora Receiver Code for Raspberry Pi: (Download the required libraries from here)

from time import sleep
from SX127x.LoRa import *
from SX127x.board_config import BOARD
import requests
import json

environmentVariables = open('./environment.json', "r")

environmentVariablesJson = json.loads(environmentVariables.read())

thingsSpeakWriteKey = environmentVariablesJson["ts_write_key"]
thingsSpeakReadKey = environmentVariablesJson["ts_read_key"]

environmentVariables.close()

propertyToField = {
    "presence": "field1",
    "humidity": "field2",
    "temperature": "field3",
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


    def on_rx_done(self):
        self.clear_irq_flags(RxDone=1)
        payload = ((bytes)(self.read_payload(nocheck=True))).decode("utf-8", 'ignore')

        payload = escapeString(payload)

        print("\nReceived: ")
        print(repr(payload))

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
            response = requests.get(f'https://api.thingspeak.com/update?api_key={thingsSpeakWriteKey}&{requestPayload}')
            print(response)
        else:
            print("Failed to decode message.")


lora = LoRaRcvCont(verbose=True)
lora.set_mode(MODE.STDBY)

#  Medium Range  Defaults after init are 434.0MHz, Bw = 125 kHz, Cr = 4/5, Sf = 128chips/symbol, CRC on 13 dBm
lora.set_pa_config(pa_select=1)

try:
    print("started")
    lora.start()
except KeyboardInterrupt:
    sys.stdout.flush()
    print("")
    sys.stderr.write("KeyboardInterrupt\n")
finally:
    sys.stdout.flush()
    print("")
    lora.set_mode(MODE.SLEEP)
    BOARD.teardown()