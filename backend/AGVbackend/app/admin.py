from django.contrib import admin
from .models import AGV, Mission,Location

admin.site.register(AGV)
admin.site.register(Mission)
admin.site.register(Location)
#admin.site.register(PayloadOption)