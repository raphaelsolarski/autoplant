from django.contrib import admin

from .models import Measurement, WaterUnit, SensorUnit, CyclicSchedule, ScheduledWatering


@admin.register(WaterUnit)
class WaterUnitAdmin(admin.ModelAdmin):
    pass


@admin.register(SensorUnit)
class SensorUnitAdmin(admin.ModelAdmin):
    pass


@admin.register(Measurement)
class MeasurementAdmin(admin.ModelAdmin):
    list_display = ('sensor_unit', 'type', 'date', 'value')


@admin.register(CyclicSchedule)
class CyclicScheduleAdmin(admin.ModelAdmin):
    pass


@admin.register(ScheduledWatering)
class ScheduledWateringAdmin(admin.ModelAdmin):
    pass
