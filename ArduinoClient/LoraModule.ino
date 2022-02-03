//Arduino Raspberry Pi wireless Comunnication through LoRa - SX1278
//Send 0 to 9 from Arduino through Radio head LoRa without ACK
//Code for: www.circuitdigest.com
//Dated: 19-4-20198

#include <SPI.h> //Import SPI library
#include <RH_RF95.h> // RF95 from RadioHead Library
#include <Arduino.h>

using namespace std;

#define RFM95_CS 10 //CS if Lora connected to pin 10
#define RFM95_RST 9 //RST of Lora connected to pin 9
#define RFM95_INT 3 //INT of Lora connected to pin 3

// Change to 434.0 or other frequency, must match RX's freq!
#define RF95_FREQ 434.0

// Singleton instance of the radio driver
RH_RF95 rf95(RFM95_CS, RFM95_INT);

void SetupLoraModule()
{
    Serial.println("Beginning LORA init.");
    pinMode(RFM95_RST, OUTPUT);
    digitalWrite(RFM95_RST, LOW);
    delay(10);
    digitalWrite(RFM95_RST, HIGH);
    delay(10);

    while (!rf95.init()) {
        Serial.println("LORA init failed.");
        while (1);
    }

    //Set the default frequency 434.0MHz
    if (!rf95.setFrequency(RF95_FREQ)) {
        Serial.println("Setting LORA frequency failed.");
        while (1);
    }

    rf95.setTxPower(18); //Transmission power of the Lora Module
    Serial.println("Finished LORA init.");
}

void SendRadioMessage(const String message)
{
    Serial.print("Started transmitting message: ");
    Serial.println(message);

    int n = message.length();

    // declaring character array
    char char_array[n + 1];

    // copying the contents of the
    // string to char array
    strcpy(char_array, message.c_str());

    rf95.send((uint8_t*)char_array, message.length());
    rf95.setModeRx();

    Serial.print("Finished transmitting.");
}
