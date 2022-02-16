#include <Arduino.h>

#define pirPin 2

int val = 0;
bool motionState = false;

void SetupMotionSensor() {
    pinMode(pirPin, INPUT);
}

int GetPresenceState() {
    val = digitalRead(pirPin);
    int presence = 0;

    if (val == HIGH) {
        presence = 1;
    }

    return presence;
}
