#include <Arduino.h>
#include <WiFi.h>
#include <WiFiClientSecure.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>
#include <time.h>
#include <string.h>
#include <stdio.h>

#include "config.h"
#include "motor.h"
#include "mqtt_handler.h"

static WiFiClientSecure secureClient;
static PubSubClient mqttClient(secureClient);


static unsigned long lastWifiAttempt=0;
static unsigned long lastMqttAttempt=0;

static const int WIFI_RETRY=5000;
static const int MQTT_RETRY=3000;

static void subscribeTopics(){
    mqttClient.subscribe(topic_order,1);
    mqttClient.subscribe(topic_action,1);


}
static void callback(char* topic,byte* payload,unsigned int length){
    Serial.print("topic");
    Serial.println("topic");
    JsonDocument doc;

    // Phân tích JSON nhận được
    DeserializationError jsonError =
        deserializeJson(doc, payload, length);

    if (jsonError) {
        Serial.println("JSON khong hop le");
        return;
    }
    if(strcmp(topic,topic_action)==0){         //hai chuỗi gióng hết nhau
        const char* receivedRobotId=doc["robotId"]|"";
        const char* action = doc["action"] | "";
        if (strcmp(receivedRobotId, robot_id) != 0) {
            Serial.println("Sai robotId");
            return;
        }
        Serial.print("Nhan action: ");
        Serial.println(action);

        if (strcmp(action, "STOP") == 0)
        {
            stop();
            Serial.println("AGV da dung");
        }
        else
        {
            Serial.println("Action khong hop le");
        }

    }
    if(strcmp(topic,topic_order)==0){
        
    }
}




static void reconnectWiFi(){
    if(WiFi.status()==WL_CONNECTED){
        return;
    }

    unsigned now=millis();
    if(now-lastWifiAttempt<WIFI_RETRY){
        return;
    }
    lastWifiAttempt=now;
    Serial.print("connecting ....");
    WiFi.disconnect();
    WiFi.begin(ssid,password);
};


static void reconnectMQTT(){
    if (WiFi.status() != WL_CONNECTED) {
        return;
    }
    if (mqttClient.connected()) {
        return;
    }
    unsigned long now = millis();
    if (now - lastMqttAttempt < MQTT_RETRY) {
        return;
    }
    lastMqttAttempt = now;
    Serial.println("Connecting to MQTT...");
    // Client ID phải duy nhất với mỗi kết nối
    char clientId[64];
    snprintf(clientId,sizeof(clientId),"%s-ESP32",robot_id);
    if (mqttClient.connect(clientId,mqtt_user,mqtt_password)) {
        Serial.println("MQTT connected!");
        subscribeTopics();
    } else {
        Serial.print("MQTT connection failed. State: ");
        Serial.println(mqttClient.state());
    }
};

void mqttSetup() {
    initMqttTopics();
    WiFi.mode(WIFI_STA);
    WiFi.begin(ssid,password);

}
