#include <SPI.h> 
#include <LoRa.h> 
#include <Arduino.h>

void SetupLora()
{
    while (!LoRa.begin(434E6)) {
    }
    
    LoRa.setSpreadingFactor(10);
    LoRa.setTxPower(20);
    LoRa.setSignalBandwidth(62.5E3);
    LoRa.enableCrc();
}

void SendRadioMessage(const char* char_array)
{
    LoraWake();
    
    LoRa.beginPacket();
    LoRa.print(char_array);
    LoRa.endPacket();

    LoraSleep;
}

void LoraSleep()
{
    LoRa.sleep();
}

void LoraWake()
{
    LoRa.idle();
}
