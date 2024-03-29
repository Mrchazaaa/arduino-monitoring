from datetime import datetime, timedelta
from SX127x.LoRa import *
from SX127x.constants import *
from SX127x.board_config import BOARD
import logging
import SX127x
import json
import importlib

def escapeString(input):
    escapes = ''.join([chr(char) for char in range(0, 32)])
    translator = str.maketrans('', '', escapes)
    return input.translate(translator)

class LoraReceiver(LoRa):
    disposed = False

    def __init__(self, verbose, logger, dataLogger, instanceId):
        self.spi = BOARD.SpiDev()              # init and get the baord's SPI
        BOARD.setup()
        BOARD.reset()
        super(LoraReceiver, self).__init__(verbose)
        self.set_dio_mapping([0] * 6)
        self.logger = logger
        self.dataLogger = dataLogger
        self.lastSuccesfulTransmissionTimestamp = None
        self.instanceId = instanceId

    def start(self):
        self.logger.info("starting lora receiver")
        self.set_mode(MODE.STDBY)
        #  Medium Range  Defaults after init are 434.0MHz, Bw = 125 kHz, Cr = 4/5, Sf = 128chips/symbol, CRC on 13 dBm
        self.set_pa_config(pa_select=1)
        self.set_spreading_factor(10)
        self.set_rx_crc(True)
        self.set_bw(BW.BW62_5)

        self.reset_ptr_rx()
        self.set_mode(MODE.RXCONT)

    def has_received_successfully_in_last(self, minutes):
        self.logger.info(f'Computing \'has received successsfully request\' given last transmission timestamp {self.lastSuccesfulTransmissionTimestamp}.')
        return (self.lastSuccesfulTransmissionTimestamp is not None) and (datetime.now() - self.lastSuccesfulTransmissionTimestamp) < timedelta(minutes=minutes)

    def dispose(self):
        # self.set_mode(MODE.SLEEP)
        self.disposed = True
        super().dispose()
        BOARD.teardown()
        importlib.reload(SX127x)

    def on_payload_crc_error(self):
        irqFlags = self.get_irq_flags()
        payload = ((bytes)(self.read_payload(nocheck=False))).decode("utf-8", 'ignore')
        rxIsGood = self.rx_is_good()
        self.logger.info(f'rx is good: {rxIsGood} {payload} {"CRC Error encountered"} irq flags: {irqFlags}.')

    def on_rx_done(self):
        self.logger.info(f'Message received for instance {self.instanceId}.')

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

            self.dataLogger.log(logging.DEBUG, payloadObject)

            self.lastSuccesfulTransmissionTimestamp = datetime.now()
        except BaseException as err:
            message = "Receive error: {0}".format(err)
            self.logger.error(f'{message}.')

    def on_rx_timeout(self):
        self.logger.info('RX timeout.')

