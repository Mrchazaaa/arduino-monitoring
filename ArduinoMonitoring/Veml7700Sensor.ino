#include "Adafruit_VEML7700.h"
#include "LowPower.h"

Adafruit_VEML7700 veml = Adafruit_VEML7700();

void SetupLuxSensor()
{
    while(!veml.begin()) {
        delay(500);
    }
    veml.setGain(VEML7700_GAIN_1);
    veml.setIntegrationTime(VEML7700_IT_800MS);
}

void VemlSleep() {
  veml.enable(true);
}

void VemlWake() {
  veml.enable(false);
}

float GetLuxReading()
{
    float lux;

    lux = veml.readLuxNormalized();

    return lux;
}
