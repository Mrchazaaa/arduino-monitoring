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
    Serial.println("Began reading DHT22 sensor.");
    int chk = DHT.read22(DHT22_PIN);

    Serial.print("Finished reading DHT22 sensor: ");
    
    switch (chk)
    {
    case DHTLIB_OK:
        Serial.println("OK.");
        break;
    case DHTLIB_ERROR_CHECKSUM:
        Serial.println("Checksum error.");
        break;
    case DHTLIB_ERROR_TIMEOUT:
        Serial.println("Time out error.");
        break;
    case DHTLIB_ERROR_CONNECT:
        Serial.println("Connect error.");
        break;
    case DHTLIB_ERROR_ACK_L:
        Serial.println("Ack Low error.");
        break;
    case DHTLIB_ERROR_ACK_H:
        Serial.println("Ack High error.");
        break;
    default:
        Serial.println("Unknown error.");
        break;
    }
}

float GetLastHumidityReading() {
    // Reading temperature or humidity takes about 250 milliseconds!
    // Sensor readings may also be up to 2 seconds 'old' (its a very slow sensor)

    float humidity = DHT.humidity;

    Serial.print("Read humidity: ");
    Serial.println(humidity);

    return humidity;
}

float GetLastTemperatureReading() {
    // Reading temperature or humidity takes about 250 milliseconds!
    // Sensor readings may also be up to 2 seconds 'old' (its a very slow sensor)
    float temp = DHT.temperature;

    Serial.print("Read temp: ");
    Serial.println(temp);

    return temp;
}
