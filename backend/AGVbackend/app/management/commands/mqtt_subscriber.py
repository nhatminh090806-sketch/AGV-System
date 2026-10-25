import paho.mqtt.client as mqtt
import json
from django.conf import settings
from django.core.management.base import BaseCommand
from app.models import AGV, Mission, Location
from django.db import transaction

def on_connect(client, userdata, flags, reason_code, properties):
    print("Ket qua ket noi:", reason_code)

    if reason_code == 0:
        print("Ket noi HiveMQ thanh cong")
        agvSub = AGV.objects.all()
        for agv in agvSub:
            # SỬA LỖI: Bắt buộc phải có chữ 'f' ở trước chuỗi để Python điền biến vào
            TOPIC = f"agv/{agv.name}/state"
            TOPIC2 = f"agv/{agv.name}/response"
            TOPIC3 = f"agv/{agv.name}/instantAction"
            TOPIC4 = f"agv/{agv.name}/connection"
            TOPIC5 = f"agv/{agv.name}/error"
            
            client.subscribe(TOPIC)
            client.subscribe(TOPIC2)
            client.subscribe(TOPIC3)
            client.subscribe(TOPIC4)
            client.subscribe(TOPIC5)
            print(f"Dang subscribe: {TOPIC} ...")
    else:
        print("Lỗi kết nối")

def handle_state(robot_id, data):
    if data.get("messageType") != "state":
        return
        
    with transaction.atomic():
        xe = AGV.objects.select_for_update().filter(name=robot_id).first()
        if xe is None:
            print("Khong tim thay AGV:", robot_id)
            return
        
        update_fields = []
        
        # 1. CHỐNG GHI ĐÈ TRẠNG THÁI: Lỗi là ưu tiên số 1
        if xe.status == "ERROR" or  xe.status=="PAUSE":
            # Nếu xe đang lỗi, ta KHÔNG cập nhật status, chỉ cập nhật pin/vận tốc
            pass 
        else:
            # Nếu xe bình thường, cho phép cập nhật trạng thái
            if not data.get("driving") and data.get("pause"):
                xe.status = "IDLE"
                update_fields.append("status")
            elif "status" in data: # Nếu firmware có gửi field status
                xe.status = data["status"]
                update_fields.append("status")

        # 2. Cập nhật các thông số khác (vẫn cập nhật kể cả khi xe đang lỗi)
        if "battery" in data:
            battery = float(data["battery"])
            if not 0 <= battery <= 100:
                raise ValueError("Battery phai tu 0 den 100")
            xe.battery = int(battery)
            update_fields.append("battery")

        if "velocity" in data:
            xe.speed = float(data["velocity"])
            update_fields.append("speed")

        if "currentNodeId" in data:
            node_id_str = data["currentNodeId"]
            location_obj = Location.objects.filter(name=node_id_str).first()
            if location_obj:
                xe.current_node = location_obj
                update_fields.append("current_node")
            else:
                print(f"Cảnh báo: Không tìm thấy Location có tên {node_id_str}")
                
        if "currentEdgeId" in data:
            xe.current_edge_id = data["currentEdgeId"]
            update_fields.append("current_edge_id")

        if update_fields:
            xe.save(update_fields=update_fields)

#giải quyết response
def handle_response(robot_id, data):
    if data.get("messageType") != "response":
        return

    updateRes_fields = []
    order = data.get("orderId")
    
    with transaction.atomic():
        mission = Mission.objects.select_for_update().filter(
            order_id=order,
            agv__name=robot_id,
        ).first()
        
        if not mission:
            return
        
        if "orderUpdateId" in data:
            status = data.get("status")
            mission.order_update_id = data["orderUpdateId"]
            updateRes_fields.append("order_update_id")
            
            valid_status = dict(Mission._meta.get_field("status").choices)
            if status not in valid_status:
                print("Trang thai khong hop le:", status)
                return

            mission.status = status
            updateRes_fields.append("status")

        if updateRes_fields:
            mission.save(update_fields=updateRes_fields)

def handle_connection(robot_id, data):
    if data.get("messageType") != "connection":
        return
        
    with transaction.atomic(): # Bắt buộc dùng atomic khi có select_for_update
        agvConnect = AGV.objects.select_for_update().filter(name=robot_id).first()
        if not agvConnect:
            return
            
        updateConnect_fields = []
        
        if "state" in data:
            connectStatus = data.get("state") # Sửa ngoặc [] thành ngoặc ()
            valid_connect = dict(AGV._meta.get_field("connection_status").choices) # Sửa Mission thành AGV
            
            if connectStatus not in valid_connect:
                return
                
            agvConnect.connection_status = connectStatus
            updateConnect_fields.append("connection_status") # Append đúng tên cột trong DB

        if updateConnect_fields:
            agvConnect.save(update_fields=updateConnect_fields)

def handle_error(robot_id, data):
    # 1. Kiểm tra loại bản tin
    if data.get("messageType") != "error":
        return
        
    with transaction.atomic():
        # 2. Tìm xe
        xe = AGV.objects.select_for_update().filter(name=robot_id).first()
        if not xe:
            print("Khong tim thay AGV:", robot_id)
            return
            
        # 3. Ép trạng thái xe thành ERROR
        xe.status = "ERROR"
        xe.save(update_fields=["status"])
        
        print(f"Xe {robot_id} đã bị đổi trạng thái thành ERROR do phần cứng báo lỗi!")

def handle_instantAction(robot_id, data):
    with transaction.atomic(): # BẮT BUỘC PHẢI CÓ
        xe = AGV.objects.select_for_update().filter(name=robot_id).first()
        
        if not xe:
            print("Khong tim thay AGV:", robot_id)
            return
            
        action = data.get("action")
        if action:
            xe.status = action
            xe.save(update_fields=["status"])


def on_message(client,userdata,msg):
    try:
      text=msg.payload.decode("utf-8")
      data=json.loads(text)
      robot_id=data.get("robotId")

      if msg.topic.endswith("/state"):
        handle_state(robot_id,data)
      elif msg.topic.endswith("/response"):
        handle_response(robot_id,data)
      elif msg.topic.endswith("/connection"):
        handle_connection(robot_id,data)
      elif msg.topic.endswith("/error"):
        handle_error(robot_id,data)
      elif msg.topic.endswith("/instantAction"):
        handle_instantAction(robot_id,data)

    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        print("Loi doc message:", e)

    except AGV.DoesNotExist:
        print("Khong tim thay AGV")

    except Mission.DoesNotExist:
        print("Khong tim thay Mission")

    except (ValueError, TypeError, KeyError) as e:
        print("Du lieu MQTT khong hop le:", e)

    except Exception as e:
        print("Loi xu ly MQTT:", e)
      
class Command(BaseCommand):
    help = "MQTT subscriber cho he thonxe"

    def handle(self, *args, **options):
        client = mqtt.Client(
            callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
            client_id="django_agv_subscriber",
        )

        client.username_pw_set(
            settings.MQTT_USERNAME,
            settings.MQTT_PASSWORD,
        )

        client.tls_set()

        client.on_connect = on_connect
        client.on_message = on_message

        print("Dang ket noi HiveMQ...")

        client.connect(
            settings.MQTT_HOST,
            settings.MQTT_PORT,
            keepalive=60,
        )

        print("Dang chay MQTT subscriber...")

        client.loop_forever()