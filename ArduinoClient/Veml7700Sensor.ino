// This file exposes methods used to read lux levels from a Veml7700 sensor.
// It depends on https://github.com/DFRobot/DFRobot_VEML7700.

#include <Wire.h>
#include "DFRobot_VEML7700.h"
#include <Arduino.h>

DFRobot_VEML7700 als;

void SetupLuxSensor()
{
    Serial.println("Began veml init.");
    als.begin();
    Serial.println("Finished veml init.");
}

float GetLuxReading()
{
    Serial.println("Began reading lux.");

    float lux;

    als.getALSLux(lux);

    Serial.print("Read lux: ");
    Serial.println(lux);

    return lux;
}
