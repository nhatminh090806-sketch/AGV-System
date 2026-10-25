from rest_framework.exceptions import ValidationError
from .models import AGV, Mission
from .mqtt_client import (
    build_order_payload,
    build_instant_action_payload,
    publish_message
)

def stop_all_agvs():
    agvs = AGV.objects.all()
    sent_count = 0
    failed_agvs = []
    
    for agv in agvs:
        topic = f"agv/{agv.name}/instant_action"
        payload = build_instant_action_payload(agv.name, "STOP")   
        try:
            publish_message(topic, payload)
            sent_count += 1
        except Exception:
            #
            failed_agvs.append(agv.name)

    return {
        "sent_count": sent_count,
        "failed_agvs": failed_agvs
    }

def create_mission(validated_data):
    agv = validated_data["agv"]

    # 1. Kiểm tra AGV đã có nhiệm vụ đang thực hiện chưa
    if (
        agv.current_mission is not None
        and agv.current_mission.status == "EXECUTING"
    ):
        raise ValidationError(
            "AGV đang thực hiện nhiệm vụ khác."
        )

    # 2. Tạo Mission trong database trước
    mission = Mission.objects.create(
        **validated_data,
        status="CREATED",
    )

    # 3. Tạo order_id dựa trên ID của Mission
    mission.order_id = f"ORD{mission.id:03d}"
    mission.save(update_fields=["order_id"])

    # 4. Tạo payload và topic MQTT
    topic, payload = build_order_payload(mission)

    # 5. Gửi nhiệm vụ đến AGV
    try:
        publish_message(topic, payload)

    except Exception as e:
        mission.status = "FAILED"
        mission.save(update_fields=["status"])

        raise ValidationError(
            f"Gửi nhiệm vụ qua MQTT thất bại: {e}"
        )

    # 6. Cập nhật trạng thái khi gửi thành công
    mission.status = "SENT"
    mission.save(update_fields=["status"])

    return mission