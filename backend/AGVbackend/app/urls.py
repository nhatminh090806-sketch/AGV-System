from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    AGVViewSet,
    MissionViewSet,
    LocationViewSet,
)

router = DefaultRouter()
router.register("agv", AGVViewSet)
router.register("mission", MissionViewSet)
router.register("location", LocationViewSet)
#router.register("payload-options", PayloadOptionViewSet)
urlpatterns = [
    path("", include(router.urls)),
]