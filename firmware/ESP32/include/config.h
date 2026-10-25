
#ifndef CONFIG_H
#define CONFIG_H
#include <Arduino.h>
#include <WiFi.h>
#include <WebServer.h>


// Wi-Fi STA
extern const char* ssid;
extern const char* password;


// MQTT Broker - HiveMQ Cloud
extern const char* mqtt_broker;
extern const int mqtt_port;
extern const char* mqtt_user;
extern const char* mqtt_password;

// Robot ID
extern const char* robot_id;

// MQTT topics
extern char topic_order[64];
extern char topic_response[64];
extern char topic_action[64];
extern char topic_state[64];
extern char topic_connection[64];
extern char topic_error[64];

void initMqttTopics();

// Cấu hình tốc độ và động cơ
extern const int basespeed;

extern const int ENA;
extern const int in1;
extern const int in2;
extern const int ENB;
extern const int in3;
extern const int in4;

// Cảm biến dò line
extern const int s0;
extern const int s1;
extern const int s2;
extern const int s3;
extern const int s4;

// Biến trạng thái vạch và PID
extern int l0, l1, l2, l3, l4;

extern int P, Kp;
extern int I, Ki;
extern int D, Kd;

extern int PID_value;
extern int error;
extern int previous_error;
extern int last_direction;

#endif
