# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.contrib.auth.models import User
from apps.authentication.models import AuthGroup

class Sensor(models.Model):
    name = models.CharField(max_length=30, blank=True, null=True)
    created = models.DateTimeField()
    last_updated = models.DateTimeField(blank=True, null=True)
    mac_address = models.CharField(unique=True, max_length=30)
    last_humidity = models.PositiveSmallIntegerField(blank=True, null=True)
    last_temperature_f = models.FloatField(blank=True, null=True)
    uuid = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'sensor'


class SensorData(models.Model):
    temperature_f = models.FloatField()
    sensor = models.ForeignKey(Sensor, models.DO_NOTHING, db_column='sensor')
    created = models.DateTimeField()
    humidity = models.PositiveSmallIntegerField()

    class Meta:
        managed = False
        db_table = 'sensor_data'


class AuthSensorGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    sensor = models.ForeignKey('Sensor', models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_sensor_groups'
        unique_together = (('sensor', 'group'),)

    def exists(self):
        if AuthSensorGroups.objects.get(sensor=self.sensor):
            return True
        return False