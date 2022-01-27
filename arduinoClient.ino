//Arduino Raspberry Pi wireless Comunnication through LoRa - SX1278
//Send 0 to 9 from Arduino through Radio head LoRa without ACK
//Code for: www.circuitdigest.com
//Dated: 19-4-20198

#include <SPI.h> //Import SPI librarey
#include <RH_RF95.h> // RF95 from RadioHead Librarey

using namespace std;

#define RFM95_CS 10 //CS if Lora connected to pin 10
#define RFM95_RST 9 //RST of Lora connected to pin 9
#define RFM95_INT 3 //INT of Lora connected to pin 3

// Change to 434.0 or other frequency, must match RX's freq!
#define RF95_FREQ 434.0

// Singleton instance of the radio driver
RH_RF95 rf95(RFM95_CS, RFM95_INT);

void setup()
{
  Serial.println("init started");

  //Initialize Serial Monitor
  Serial.begin(9600);

  // Reset LoRa Module
  pinMode(RFM95_RST, OUTPUT);
  digitalWrite(RFM95_RST, LOW);
  delay(10);
  digitalWrite(RFM95_RST, HIGH);
  delay(10);

  //Initialize LoRa Module
  while (!rf95.init()) {
    Serial.println("init failed");
    while (1);
  }


  //Set the default frequency 434.0MHz
  if (!rf95.setFrequency(RF95_FREQ)) {
    Serial.println("setFrequency failed");
    while (1);
  }

  rf95.setTxPower(18); //Transmission power of the Lora Module

  Serial.println("init passed");
}

char value = 50;

void serialPrint(const char* message)
{
    Serial.print(message);
    return;
}

void loop()
{
  Serial.print("Send: ");
  Serial.print(char(value));
  Serial.print("\n");
  char radiopacket[1] = { char(value) };
  rf95.send((uint8_t*)radiopacket, 1, serialPrint);
  
  Serial.print("Waiter");
  rf95.setModeRx();
  //rf95.waitPacketSent();

  Serial.print("Sent: ");
  Serial.print(value);
  Serial.print("\n");

  Serial.print("Waiting...\n");
  delay(1000);
  Serial.print("Waited\n");
  value++;
  if (value > '9')
    value = 48;
}
