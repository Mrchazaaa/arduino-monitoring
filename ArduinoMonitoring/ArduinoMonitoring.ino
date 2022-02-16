#include <Arduino.h>
#include <ArduinoJson.h>
#include "LowPower.h"

void setup()
{
    while (!Serial) { delay(10); }
    Serial.begin(9600);

    SetupLuxSensor();
    SetupMotionSensor();

    SetupLora();

    delay(1000);
}

void SleepForMinutes(float minutes)
{
    int totalSeconds = (minutes) * 60;

    for (int i = 0; i < totalSeconds; i+=8)
    {
        LowPower.powerDown(SLEEP_8S, ADC_OFF, BOD_OFF);
    }
}

void loop()
{
    LoraWake();
    VemlWake();

    float lux = GetLuxReading();
    ReadFromHumidityAndTemperatureSensor();
    float humidity = GetLastHumidityReading();
    float temp = GetLastTemperatureReading();
    int presence = GetPresenceState();

    StaticJsonDocument<50> jsonData;
    jsonData["hmd"] = humidity;
    jsonData["tmp"] = temp;
    jsonData["psc"] = presence;
    jsonData["lux"] = lux;

    char message[50];
    serializeJson(jsonData, message);

    SendRadioMessage(message);

    VemlSleep();
    LoraSleep();

    SleepForMinutes(10);
}
