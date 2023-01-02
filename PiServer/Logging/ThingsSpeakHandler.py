import requests
from logging import StreamHandler

class ThingsSpeakHandler(StreamHandler):

    def __init__(self, logger, thingsSpeakWriteKey):
        StreamHandler.__init__(self)
        self.logger = logger
        self.thingsSpeakWriteKey = thingsSpeakWriteKey
        self.propertyToField = {
            "psc": "field1",
            "hmd": "field2",
            "tmp": "field3",
            "lux": "field4"
        }

    def emit(self, record):
        requestPayload = ""
        for key in record.msg:
            if key in self.propertyToField:
                requestPayload += f'{self.propertyToField[key]}={record.msg[key]}&'

        if len(requestPayload) > 0:
            request = f'https://api.thingspeak.com/update?api_key={self.thingsSpeakWriteKey}&{requestPayload}'
            self.logger.info(f'request: {request}')
            response = requests.get(request)
            self.logger.info(f'response: {response}')
        else:
            self.logger.error(f'Failed to decode message.')