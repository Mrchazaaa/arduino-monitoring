from time import sleep
from SX127x.LoRa import *
from SX127x.constants import *
import requests
import json
from datetime import datetime

def escapeString(input):
    escapes = ''.join([chr(char) for char in range(0, 32)])
    translator = str.maketrans('', '', escapes)
    return input.translate(translator)

class LoraReceiver(LoRa):
    def __init__(self, verbose, wks, propertyToField, thingsSpeakWriteKey):
        super(LoraReceiver, self).__init__(verbose)
        self.set_mode(MODE.SLEEP)
        self.set_dio_mapping([0] * 6)
        self.wks = wks
        self.propertyToField = propertyToField
        self.thingsSpeakWriteKey = thingsSpeakWriteKey

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
        payload = ((bytes)(self.read_payload(nocheck=True))).decode("utf-8", 'ignore')
        rxIsGood = self.rx_is_good()
        self.wks.append_table(values=[time, rxIsGood, payload, "CRC Error encountered", irqFlags])
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
            rxIsGood = self.rx_is_good()
            print("\nrx is good: ")
            print(rxIsGood)
            print("\nRSSI: ")
            print(rsi)
            print("\nReceived: ")
            print(repr(payload))

            self.wks.append_table(values=[time, rsi, rxIsGood, payload])

            self.set_mode(MODE.SLEEP)
            self.reset_ptr_rx()
            self.set_mode(MODE.RXCONT)

            payloadObject = json.loads(payload)
            requestPayload = ""

            for key in payloadObject:
                if key in self.propertyToField:
                    requestPayload += f'{self.propertyToField[key]}={payloadObject[key]}&'

            if len(requestPayload) > 0:
                # post data to dashboard
                request = f'https://api.thingspeak.com/update?api_key={self.thingsSpeakWriteKey}&{requestPayload}'
                print(request)
                response = requests.get(request)
                print(response)
            else:
                print("Failed to decode message.")
        except BaseException as err:
            message = "Receive error: {0}".format(err)
            print(message)
            self.wks.append_table(values=[time, message])
