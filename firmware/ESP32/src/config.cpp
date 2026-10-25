#include <Arduino.h>
#include "config.h"

// Wi-Fi STA
const char* ssid = "Nm";
const char* password = "1234567890";

WebServer server(80);

// ===== MQTT Broker: HiveMQ Cloud =====
const char* mqtt_broker =
    "2bf5ff7bb1314f12afb9c5d5c54208be.s1.eu.hivemq.cloud";

const int mqtt_port = 8883;
const char* mqtt_user = "minh_subscriber";
const char* mqtt_password = "Nhatminh0908@";

// Robot ID: cấu hình riêng cho từng ESP32
const char* robot_id = "AGV001";

// MQTT topics
char topic_order[64];
char topic_response[64];
char topic_action[64];
char topic_state[64];
char topic_connection[64];
char topic_error[64];

// Tạo topic dựa trên Robot ID
void initMqttTopics() {
    snprintf(topic_order, sizeof(topic_order),
             "agv/%s/order", robot_id);

    snprintf(topic_response, sizeof(topic_response),
             "agv/%s/response", robot_id);

    snprintf(topic_action, sizeof(topic_action),
             "agv/%s/instant_action", robot_id);

    snprintf(topic_state, sizeof(topic_state),
             "agv/%s/state", robot_id);

    snprintf(topic_connection, sizeof(topic_connection),
             "agv/%s/connection", robot_id);

    snprintf(topic_error, sizeof(topic_error),
             "agv/%s/error", robot_id);
}

// Cấu hình tốc độ và động cơ
const int basespeed = 200;

const int ENA = 27;
const int in1 = 25;
const int in2 = 26;
const int ENB = 33;
const int in3 = 14;
const int in4 = 32;

// Cảm biến dò line
const int s0 = 34;
const int s1 = 35;
const int s2 = 4;
const int s3 = 16;
const int s4 = 17;

// Biến trạng thái vạch và PID
int l0 = 0, l1 = 0, l2 = 0, l3 = 0, l4 = 0;

int P = 0, Kp = 10;
int I = 0, Ki = 0;
int D = 0, Kd = 0;

int PID_value = 0;
int error = 0;
int previous_error = 0;
int last_direction = 0;
