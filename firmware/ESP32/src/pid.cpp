#include "config.h"
#include "pid.h"

int calculatePID(int error){
    static int integral = 0;
    static int previousError = 0;

    int P = error;
    integral += error;
    int I = integral;
    int D = error - previousError;
    int PID_value = Kp * P + Ki * I + Kd * D;
    previousError = error;
    return PID_value;

}