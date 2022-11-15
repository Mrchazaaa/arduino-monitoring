import requests

class ThingsSpeakLogger:
    def __init__(self, logger, thingsSpeakWriteKey):
        self.logger = logger
        self.thingsSpeakWriteKey = thingsSpeakWriteKey
        self.propertyToField = {
            "psc": "field1",
            "hmd": "field2",
            "tmp": "field3",
            "lux": "field4"
        }

    def log(self, payloadObject):
        requestPayload = ""
        for key in payloadObject:
            if key in self.propertyToField:
                requestPayload += f'{self.propertyToField[key]}={payloadObject[key]}&'

        if len(requestPayload) > 0:
            request = f'https://api.thingspeak.com/update?api_key={self.thingsSpeakWriteKey}&{requestPayload}'
            self.logger.info(f'request: {request}')
            response = requests.get(request)
            self.logger.info(f'response: {response}')
        else:
            self.logger.error(f'Failed to decode message.')