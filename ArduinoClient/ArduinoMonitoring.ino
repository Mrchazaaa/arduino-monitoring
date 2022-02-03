#include <Arduino.h>
#include <Veml7700Sensor.ino>
#include <Dht22Sensor.ino>
#include <HcSr501.ino>>
#include <LoraModule.ino>

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
    String message = "{\"humidity\": ";
    message.concat(humidity);
    message.concat(",\"temp\": ");
    message.concat(temp);
    message.concat(",\"lux\": ");
    message.concat(lux);
    message.concat(",\"presence\": ");
    message.concat(presence);
    message.concat("}");

    SendRadioMessage(message);

    Serial.println("Finished control loop.");
}
