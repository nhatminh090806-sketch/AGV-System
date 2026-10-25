from rest_framework import serializers
from .models import AGV, Mission, Location


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ["id", "name"]

#class PayloadOptionSerializer(serializers.ModelSerializer):
#    class Meta:
#        model = PayloadOption
#        fields = ["id", "amount"]

class AGVSerializer(serializers.ModelSerializer):
    class Meta:
        model = AGV
        fields = "__all__"

class MissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Mission
        fields = [
            "id",
            "agv",
            "start_point",
            "end_point",
            "start_time",
            "status",
            "progress",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "status",
            "progress",
            "created_at",
            "updated_at",
        ]