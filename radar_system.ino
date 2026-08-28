#include <Servo.h>

Servo servo;
const int trigPin = 9;
const int echoPin = 10;

void setup() {
    Serial.begin(9600);
    servo.attach(6);
    pinMode(trigPin, OUTPUT);
    pinMode(echoPin, INPUT);
}

long getDistance() {
    digitalWrite(trigPin, LOW);
    delayMicroseconds(2);
    digitalWrite(trigPin, HIGH);
    delayMicroseconds(10);
    digitalWrite(trigPin, LOW);
    long duration = pulseIn(echoPin, HIGH);
    return duration * 0.034 / 2;  // Convert to cm
}

void loop() {
    for (int angle = 0; angle <=180; angle += 10) {
        servo.write(angle);
        delay(5);
        long distance = getDistance();
        Serial.print(angle);
        Serial.print(",");
        Serial.println(distance);
    }
    
    for (int angle = 180; angle >= 0; angle -= 10) {
        servo.write(angle);
        delay(5);
        long distance = getDistance();
        Serial.print(angle);
        Serial.print(",");
        Serial.println(distance);
    }
}
