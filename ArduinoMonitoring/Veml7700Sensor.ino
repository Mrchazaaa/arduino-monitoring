// This file exposes methods used to read lux levels from a Veml7700 sensor.
// It depends on https://github.com/DFRobot/DFRobot_VEML7700.

#include "Adafruit_VEML7700.h"
#include "LowPower.h"

Adafruit_VEML7700 veml = Adafruit_VEML7700();

void SetupLuxSensor()
{
    Serial.println("Began veml init.");
    while(!veml.begin()) {
        delay(500);
        Serial.println("veml init failed.");  
    }
    veml.setGain(VEML7700_GAIN_1);
    veml.setIntegrationTime(VEML7700_IT_800MS);
    Serial.println("Finished veml init.");
}

void VemlSleep() {
  Serial.println("veml going to sleep.");
  veml.enable(true);
}

void VemlWake() {
  Serial.println("veml waking up.");
  veml.enable(false);
}

float GetLuxReading()
{
    Serial.println("Began reading lux.");

    float lux;

    lux = veml.readLux();

    Serial.print("Read lux: ");
    Serial.println(lux);

    return lux;
}
