
from rest_framework import viewsets, status
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import AGV, Mission, Location
from .serializers import (
    AGVSerializer,
    MissionSerializer,
    LocationSerializer,
)
from .services import stop_all_agvs, create_mission


class LocationViewSet(ReadOnlyModelViewSet):
    queryset = Location.objects.all().order_by("id")
    serializer_class = LocationSerializer


class AGVViewSet(viewsets.ModelViewSet):
    queryset = AGV.objects.all()
    serializer_class = AGVSerializer

    @action(detail=False, methods=["post"])
    def stop_all(self, request):
        result = stop_all_agvs()

        response_status = (
            status.HTTP_200_OK
            if not result["failed_agvs"]
            else status.HTTP_502_BAD_GATEWAY
        )

        return Response(
            {
                "message": "Đã xử lý yêu cầu STOP",
                **result,
            },
            status=response_status,
        )


class MissionViewSet(viewsets.ModelViewSet):
    queryset = Mission.objects.all()
    serializer_class = MissionSerializer

    def perform_create(self, serializer):
        mission = create_mission(serializer.validated_data)  #tạo json chuyển sang cho createmission
        serializer.instance = mission                        