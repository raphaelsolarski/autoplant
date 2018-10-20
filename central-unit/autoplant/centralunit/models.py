from django.db import models
from django.utils.translation import ugettext_lazy as _


class WaterUnit(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=40)

    def __str__(self):
        return '{} {}'.format(self.id, self.name)

    class Meta:
        verbose_name = _('Water unit')
        verbose_name_plural = _('Water units')


class SensorUnit(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=40)

    class Meta:
        verbose_name = _('Sensor unit')
        verbose_name_plural = _('Sensor units')


class Measurement(models.Model):
    sensor_unit = models.ForeignKey(SensorUnit, on_delete=models.DO_NOTHING, max_length=40,
                                    verbose_name=_('Sensor unit'))
    type = models.CharField(max_length=40, verbose_name=_('Type'))
    date = models.DateTimeField(verbose_name=_('Date'))
    value = models.FloatField(verbose_name=_('Value'))

    def __str__(self):
        return '{} {} {} {}'.format(self.sensor_unit, self.type, self.date, self.value)

    class Meta:
        verbose_name = _('Measurement')
        verbose_name_plural = _('Measurements')


class CyclicSchedule(models.Model):
    water_unit = models.ForeignKey(WaterUnit, on_delete=models.DO_NOTHING, max_length=40, verbose_name=_('Water unit'))
    time = models.TimeField(verbose_name=_('Time'))
    water_amount = models.IntegerField(verbose_name=_('Water amount'))

    def __str__(self):
        return 'Water unit: {} at: {} Amount: {} ml'.format(self.water_unit, self.time, self.water_amount)

    class Meta:
        verbose_name = _('Cyclic schedule')
        verbose_name_plural = _('Cyclic schedules')


class ScheduledWatering(models.Model):
    creation_date = models.DateTimeField(auto_now_add=True, verbose_name=_('Creation date'))
    scheduled_watering_date = models.DateTimeField(verbose_name=_('Scheduled watering date'))
    watering_performed_date = models.DateTimeField(null=True, verbose_name=_('Watering performed date'))
    cyclicSchedule = models.ForeignKey(CyclicSchedule, on_delete=models.DO_NOTHING, null=True,
                                       verbose_name=_('Cyclic Schedule'))

    def __str__(self):
        return '{} {} {} {}'.format(self.scheduling_date,
                                    self.scheduled_watering_date,
                                    self.watering_performed_date,
                                    self.cyclicSchedule)

    class Meta:
        verbose_name = _('Scheduled watering')
        verbose_name_plural = _('Scheduled waterings')
