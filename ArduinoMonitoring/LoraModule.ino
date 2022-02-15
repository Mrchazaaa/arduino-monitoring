#include <SPI.h> 
#include <LoRa.h> 
#include <Arduino.h>

void SetupLora()
{
    Serial.println("Beginning LORA init.");
    while (!LoRa.begin(434E6)) {
        Serial.println("LORA init failed.");
        Serial.flush();
    }

    Serial.println("Finished LORA init.");  
}

void SendRadioMessage(const char* char_array)
{
    Serial.print("Started transmitting message: ");
    Serial.println(char_array);

    LoRa.beginPacket();
    LoRa.print(char_array);
    LoRa.endPacket();
    
    Serial.println("Finished transmitting.");
}

void LoraSleep()
{
    Serial.println("Lora going to sleep.");
    LoRa.sleep();
}

void LoraWake()
{
    Serial.println("Lora waking up.");
    LoRa.idle();
}
