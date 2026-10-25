#ifndef MQTT_HANDLER_H
#define MQTT_HANDLER_H

#include <Arduino.h>

extern bool agvEnabled;

void mqttSetup();
void mqttLoop();
#endif