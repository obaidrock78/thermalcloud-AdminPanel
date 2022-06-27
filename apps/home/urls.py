# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.home import views

urlpatterns = [

    # The home page
    path('', views.dashboard, name='Dashboard'),

    # Matches any html file
    path('add_sensor', views.register_sensor, name='Add a sensor'),
    path('sensor_overview', views.sensor_overview, name='Sensor Overview'),
    path('dashboard', views.dashboard, name='Dashboard'),
    re_path(r'^.*\.*', views.pages, name='pages'),

]
