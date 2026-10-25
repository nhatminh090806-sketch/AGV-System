#include <Arduino.h>
#include"motor.h"
#include"config.h"

void initMotor(){
    pinMode(ENA, OUTPUT);
    pinMode(in1, OUTPUT);
    pinMode(in2, OUTPUT);

    pinMode(ENB, OUTPUT);
    pinMode(in3, OUTPUT);
    pinMode(in4, OUTPUT);

    stop();
}
void leftMotor(int speed){
    if(speed>=0){
        digitalWrite(in1, HIGH);
        digitalWrite(in2, LOW);
    }
    else {
        digitalWrite(in1, LOW);
        digitalWrite(in2, HIGH);
        speed = -speed;
    }
    analogWrite(ENA, constrain(speed, 0, 255));
}

void rightMotor(int speed){
    if(speed>=0){
        digitalWrite(in3, HIGH);
        digitalWrite(in4, LOW);
    }
    else {
        digitalWrite(in3, LOW);
        digitalWrite(in4, HIGH);
        speed = -speed;
    }
    analogWrite(ENB, constrain(speed, 0, 255));
}

void stop() {
    analogWrite(ENA, 0);
    analogWrite(ENB, 0);
}