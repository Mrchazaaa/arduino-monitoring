// This file exposes methods used to read lux levels from a Veml7700 sensor.
// It depends on https://github.com/DFRobot/DFRobot_VEML7700.

#include <Arduino.h>
#include "DHT.h"

#define DHTPIN 5
#define DHTTYPE DHT22

DHT dht(DHTPIN, DHTTYPE);

void SetupHumiditySensor() {
    Serial.println("Began DHT22 init.");
    dht.begin();
    Serial.println("Finished DHT22 init.");
}

float GetHumidityReading() {
    Serial.println("Began reading humidity.");

    // Reading temperature or humidity takes about 250 milliseconds!
    // Sensor readings may also be up to 2 seconds 'old' (its a very slow sensor)
    float humidity = dht.readHumidity();

    Serial.print("Read humidity: ");
    Serial.println(humidity);

    return humidity;
}

float GetTemperatureReading() {
    Serial.println("Began reading temp.");

    // Reading temperature or humidity takes about 250 milliseconds!
    // Sensor readings may also be up to 2 seconds 'old' (its a very slow sensor)
    float temp = dht.readTemperature();

    Serial.print("Read temp: ");
    Serial.println(temp);

    return temp;
}