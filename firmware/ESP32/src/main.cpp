#include <Arduino.h>
#include "config.h"
#include "motor.h"
#include "sensor.h"
#include "pid.h"
void setup(){
  Serial.begin(9600);

  initMotor();
  initSensor();
}
void loop() {
  errorCalculation();
  int PID_value = calculatePID(error);

  int left_speed = basespeed + PID_value;
  int right_speed = basespeed - PID_value;

  leftMotor(left_speed);
  rightMotor(right_speed);

}


