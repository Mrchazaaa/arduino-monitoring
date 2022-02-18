#include <SPI.h> 
#include <LoRa.h> 
#include <Arduino.h>

void SetupLora()
{
    while (!LoRa.begin(434E6)) {
    }
}

void SendRadioMessage(const char* char_array)
{
    LoRa.beginPacket();
    LoRa.print(char_array);
    LoRa.endPacket();
}

void LoraSleep()
{
    LoRa.sleep();
}

void LoraWake()
{
    LoRa.idle();
}
