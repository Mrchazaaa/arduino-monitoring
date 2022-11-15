from time import sleep
from datetime import datetime, timedelta
from SX127x.LoRa import *
from SX127x.constants import *
import json

def escapeString(input):
    escapes = ''.join([chr(char) for char in range(0, 32)])
    translator = str.maketrans('', '', escapes)
    return input.translate(translator)

class LoraReceiver(LoRa):

    def __init__(self, verbose, logger, dataLogger):
        super(LoraReceiver, self).__init__(verbose)
        self.set_mode(MODE.SLEEP)
        self.set_dio_mapping([0] * 6)
        self.logger = logger
        self.dataLogger = dataLogger
        self.lastSuccesfulTransmissionTimestamp = None

    def HasReceivedSuccessfullyInLast25Mins(self):
        return self.lastSuccesfulTransmissionTimestamp is not None and (datetime.now() - self.lastSuccesfulTransmissionTimestamp) > timedelta(minutes=25)

    def start(self):
        self.reset_ptr_rx()
        self.set_mode(MODE.RXCONT)
        while True:
            sleep(.5)
            sys.stdout.flush()

    def on_payload_crc_error(self):
        irqFlags = self.get_irq_flags()
        payload = ((bytes)(self.read_payload(nocheck=False))).decode("utf-8", 'ignore')
        rxIsGood = self.rx_is_good()
        self.logger.info(f'rx is good: {rxIsGood} {payload} {"CRC Error encountered"} irq flags: {irqFlags}.')

    def on_rx_done(self):
        self.logger.info(f'Message received.')

        try:
            self.clear_irq_flags(RxDone=1)
            payload = ((bytes)(self.read_payload(nocheck=True))).decode("utf-8", 'ignore')

            payload = escapeString(payload)

            rsi = self.get_rssi_value()
            rxIsGood = self.rx_is_good()

            self.logger.info(f'rsi: {rsi} rx is good: {rxIsGood} {payload}.')

            self.set_mode(MODE.SLEEP)
            self.reset_ptr_rx()
            self.set_mode(MODE.RXCONT)

            payloadObject = json.loads(payload)

            self.dataLogger.log(payloadObject)

            self.lastSuccesfulTransmissionTimestamp = datetime.now()
        except BaseException as err:
            message = "Receive error: {0}".format(err)
            self.logger.error(f'{message}.')

    def on_rx_timeout(self):
        self.logger.info('RX timeout.')

