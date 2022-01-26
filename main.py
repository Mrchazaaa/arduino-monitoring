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
    "light": "field4"
}

data = 1

response = requests.get(f'https://api.thingspeak.com/update?api_key={thingsSpeakWriteKey}&{propertyToField["presence"]}={data}')
print(response)