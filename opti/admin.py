from django.contrib import admin
from .models import WeeklyTransportCapacity, Slaugherhouse, Farm, WeeklyAnimalTransport, WeeklySlaughterhouseDemand, WeeklyFarmAnimalAvailability

# Register your models here.
admin.site.register(WeeklyAnimalTransport)
admin.site.register(Slaugherhouse)
admin.site.register(Farm)
admin.site.register(WeeklyFarmAnimalAvailability)
admin.site.register(WeeklySlaughterhouseDemand)
admin.site.register(WeeklyTransportCapacity)