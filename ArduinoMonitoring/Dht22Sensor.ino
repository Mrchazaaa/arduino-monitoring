// This file exposes methods used to read lux levels from a Veml7700 sensor.
// It depends on https://github.com/DFRobot/DFRobot_VEML7700.

#include <Arduino.h>

#include <dht.h>

dht DHT;

#define DHT22_PIN     5

struct
{
    uint32_t total;
    uint32_t ok;
    uint32_t crc_error;
    uint32_t time_out;
    uint32_t connect;
    uint32_t ack_l;
    uint32_t ack_h;
    uint32_t unknown;
} stat = { 0,0,0,0,0,0,0,0};


float ReadFromHumidityAndTemperatureSensor() {
    int chk = DHT.read22(DHT22_PIN);
}

float GetLastHumidityReading() {
    // Reading temperature or humidity takes about 250 milliseconds!
    // Sensor readings may also be up to 2 seconds 'old' (its a very slow sensor)

    float humidity = DHT.humidity;

    return humidity;
}

float GetLastTemperatureReading() {
    // Reading temperature or humidity takes about 250 milliseconds!
    // Sensor readings may also be up to 2 seconds 'old' (its a very slow sensor)
    float temp = DHT.temperature;

    return temp;
}
