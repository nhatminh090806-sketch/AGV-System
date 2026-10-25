import json
from datetime import datetime, timezone
import paho.mqtt.publish as publish
from django.conf import settings

_header_ids = {}

def get_header(topic, robot_id, message_type):
    _header_ids[topic] = _header_ids.get(topic, 0) + 1

    return {
        "headerId": _header_ids[topic],
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "version": "1.0.0",
        "messageType": message_type,
        "robotId": robot_id,
    }

# 1. ORDER: Backend -> Firmware
def build_order_payload(mission):
    robot_id = mission.agv.name
    topic = f"agv/{robot_id}/order"

    payload = get_header(topic, robot_id, "order")
    payload.update({
        "orderId": mission.order_id,
        "orderUpdateId": mission.order_update_id,
        "nodes": [
            {
                "nodeId": mission.start_point.name,
                "sequenceId": 0,
                "released": True,
            },
            {
                "nodeId": mission.end_point.name,
                "sequenceId": 2,
                "released": True,
            },
        ],
        "edges": [
            {
                "edgeId": (
                    f"{mission.start_point.name}_"
                    f"{mission.end_point.name}"
                ),
                "sequenceId": 1,
                "startNodeId": mission.start_point.name,
                "endNodeId": mission.end_point.name,
                "maximumSpeed": mission.maximum_speed,
            }
        ],
    })
    return payload


# 2. INSTANT ACTION: Backend -> Firmware
def build_instant_action_payload(robot_id, action):
    topic = f"agv/{robot_id}/instant_action"
    payload = get_header(topic, robot_id, "instantAction")
    payload["action"] = action
    return payload

# Gửi payload lên MQTT Broker
def publish_message(topic, payload, qos=1):
    publish.single(
        topic=topic,
        payload=json.dumps(payload),
        qos=qos,
        hostname=settings.MQTT_HOST,
        port=settings.MQTT_PORT,
        auth={
            "username": settings.MQTT_USERNAME,
            "password": settings.MQTT_PASSWORD,
        },
        tls={},
    )
