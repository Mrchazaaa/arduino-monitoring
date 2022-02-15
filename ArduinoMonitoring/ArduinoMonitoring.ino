#include <Arduino.h>
//#include <Veml7700Sensor.ino>
//#include <Dht22Sensor.ino>
//#include <HcSr501.ino>
//#include <LoraModule.ino>
#include <ArduinoJson.h>
#include "LowPower.h"

void setup()
{
    while (!Serial) { delay(10); }
    Serial.begin(9600);
    Serial.println("Init started.");

    SetupLuxSensor();
    SetupMotionSensor();

    SetupLora();
    Serial.println("Init finished.");
    Serial.flush();

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
    Serial.println("Beginning control loop.");
    Serial.flush();

    LoraWake();
    VemlWake();

    float lux = GetLuxReading();
    ReadFromHumidityAndTemperatureSensor();
    float humidity = GetLastHumidityReading();
    float temp = GetLastTemperatureReading();
    int presence = GetPresenceState();

    // construct json object
    StaticJsonDocument<200> jsonData;
    jsonData["humidity"] = humidity;
    jsonData["temperature"] = temp;
    jsonData["presence"] = presence;
    jsonData["lux"] = lux;

    char message[200];
    serializeJson(jsonData, message);

    SendRadioMessage(message);

    Serial.println("Finished control loop.");

    VemlSleep();
    LoraSleep();

    Serial.flush();
    SleepForMinutes(0.0001);
}
