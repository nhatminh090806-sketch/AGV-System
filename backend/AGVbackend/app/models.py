from django.db import models


class Location(models.Model):                          # vị trí start và end
    name = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name


#class PayloadOption(models.Model):                     #giá trị payload
   # amount = models.FloatField(unique=True)

  #  def __str__(self):
  #      return f"{self.amount} kg"


class AGV(models.Model):
    STATUS_CHOICES = [
        ("IDLE", "IDLE"),
        ("CHARGING", "CHARGING"),
        ("ERROR", "ERROR"),
        ("PAUSE","PAUSE")
    ]
    CONNECTION_CHOICES = [
        ("ONLINE", "ONLINE"),
        ("OFFLINE", "OFFLINE"),
        ("CONNECTION_BROKEN", "CONNECTION_BROKEN")
    ]

    connection_status = models.CharField(
    max_length=20,
    choices=CONNECTION_CHOICES,
    default="OFFLINE",
      )

    name = models.CharField(max_length=10, unique=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="IDLE",
    )
    battery = models.IntegerField(default=100)
    speed = models.FloatField(default=0)
    maximum_speed = models.FloatField(default=0.30)  # Tốc độ tối đa (m/s)
    # payload = models.FloatField(default=0)
    trips = models.PositiveIntegerField(default=0)
    current_node = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="agvs_current",
    )

    current_edge_id = models.CharField(
        max_length=30,
        blank=True,
        default="",
    )
    distance = models.FloatField(default=0)
    current_mission = models.ForeignKey(
        "Mission",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="current_agvs",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def is_low_battery(self):
        return self.battery < 20

    def __str__(self):
        return self.name


class Mission(models.Model):
    STATUS_CHOICES = [
        ("CREATED", "CREATED"),
        ("SENT", "SENT"),
        ("ACCEPTED", "ACCEPTED"),
        ("EXECUTING", "EXECUTING"),
        ("PAUSED", "PAUSED"),
        ("FAILED", "FAILED"),
        ("FINISHED", "FINISHED"),
        ("REJECTED", "REJECTED"),
        ("CANCELLED", "CANCELLED"),
]
    order_id = models.CharField(max_length=20, unique=True, null=True, blank=True)
    agv = models.ForeignKey(AGV,on_delete=models.CASCADE,related_name="missions")

    # Liên kết tới danh sách điểm
    start_point = models.ForeignKey(
       Location,
       on_delete=models.PROTECT,
       related_name="missions_started",
    )
    end_point = models.ForeignKey(
       Location,
       on_delete=models.PROTECT,
       related_name="missions_ended",
    )
    # Khối lượng hàng của nhiệm vụ
    #load_amount = models.FloatField(default=0)
    start_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="CREATED",
    )
    order_update_id = models.PositiveIntegerField(default=0)
    progress = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return (
            f"{self.agv.name}: "
            f"{self.start_point.name} -> {self.end_point.name}"
        )