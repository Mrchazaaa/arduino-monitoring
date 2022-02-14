#include <Arduino.h>

#define pirPin 2

int val = 0;
bool motionState = false;

void SetupMotionSensor() {
    Serial.println("Began HCSR501 init.");
    pinMode(pirPin, INPUT);
    Serial.println("Finished HCSR501 init.");
    Serial.flush();
}

int GetPresenceState() {
    Serial.println("Began reading lux.");
    val = digitalRead(pirPin);
    int presence = 0;

    if (val == HIGH) {
        presence = 1;
    }

    Serial.print("Read presence: ");
    Serial.println(presence);

    return presence;
}
