#include <Arduino.h>
#include <Veml7700Sensor.ino>
#include <Dht22Sensor.ino>
#include <HcSr501.ino>>
#include <LoraModule.ino>
#include <ArduinoJson.h>

void setup()
{
    Serial.begin(9600);
    Serial.println("Init started.");

    SetupLuxSensor();
    SetupHumiditySensor();
    SetupMotionSensor();
    SetupLoraModule();

    Serial.println("Init finished.");
}

void loop()
{
    // Wait a few seconds between measurements.
    delay(5000);

    Serial.println("Beginning control loop.");

    float lux = GetLuxReading();
    float humidity = GetHumidityReading();
    float temp = GetTemperatureReading();
    int presence = GetPresenceState();

    // construct json object
    StaticJsonDocument<500> jsonData;
    jsonData["humidity"] = humidity;
    jsonData["temperature"] = temp;
    jsonData["presence"] = presence;
    jsonData["lux"] = lux;

    char message[256];
    serializeJson(jsonData, message);

    SendRadioMessage(message);

    Serial.println("Finished control loop.");
}
