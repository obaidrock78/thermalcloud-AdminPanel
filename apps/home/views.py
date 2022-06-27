# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse

from datetime import datetime, timedelta

from apps.authentication.models import AuthUser, AuthUserGroups

from .forms import RegisterSensor
from apps.home.models import Sensor, SensorData, AuthSensorGroups


@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def register_sensor(request):
    msg = None
    success = False

    if request.method == "POST":
        form = RegisterSensor(request.POST)
        print(form)
        if form.is_valid():
#            form.save()
            mac = form.cleaned_data.get("mac")
            name = form.cleaned_data.get("name")
            real_user = AuthUser.objects.get(id=request.user.id)
            try:
                real_sensor = Sensor.objects.get(mac_address=mac)
            except Sensor.DoesNotExist:
                real_sensor = None
            if real_sensor:
                try:
                    auth_user_group = AuthUserGroups.objects.get(user=real_user)
                except AuthUserGroups.DoesNotExist:
                    auth_user_group = None
                real_group = auth_user_group.group
                if real_group:
                    try:
                        result, new_entry = AuthSensorGroups.objects.get_or_create(sensor=real_sensor, group=real_group)
                    except AuthSensorGroups.DoesNotExist:
                        result = None
                    if new_entry:
                        real_sensor.name = name
                        real_sensor.save()
                        print(result)
                        msg = 'Sensor added successfully.'
                        success = True
                        form = RegisterSensor()
                    else:
                        msg = 'Sensor is already registered with an account'
                else:
                    msg = 'User is not tied to an account'
            else:
                msg = 'Sensor does not exist'
            # return redirect("/login/")

        else:
            msg = 'Form is not valid'
    else:
        form = RegisterSensor()

    return render(request, "home/add_sensor.html", {"form": form, "msg": msg, "success": success})

    
@login_required(login_url="/login/")
def dashboard(request):
    msg = None
    success = False

    real_user = AuthUser.objects.get(id=request.user.id)
    try:
        auth_user_group = AuthUserGroups.objects.get(user=real_user)
        real_group = auth_user_group.group
    except AuthUserGroups.DoesNotExist:
        auth_user_group = None
        real_group = None
    if real_group:
        try:
            result = AuthSensorGroups.objects.select_related('sensor').filter(group=real_group)
        except AuthSensorGroups.DoesNotExist:
            result = None
        if result:
            for i in result:
                i.sensor.last_temperature_c = round(((i.sensor.last_temperature_f - 32) * (5/9)), 2)

                if i.sensor.last_temperature_f > 76:
                    i.sensor.temperature_status_color='red'
                elif i.sensor.last_temperature_f > 72:
                    i.sensor.temperature_status_color='yellow'
                elif i.sensor.last_temperature_f < 67:
                    i.sensor.temperature_status_color='blue'
                else:
                    i.sensor.temperature_status_color='green'

                
                if i.sensor.last_humidity > 70:
                    i.sensor.last_humidity_status_color='red'
                elif i.sensor.last_humidity > 60:
                    i.sensor.last_humidity_status_color='yellow'
                elif i.sensor.last_humidity < 25:
                    i.sensor.last_humidity_status_color='red'
                elif i.sensor.last_humidity < 30:
                    i.sensor.last_humidity_status_color='yellow'
                else:
                    i.sensor.last_humidity_status_color='green'
            sensor_list = result
            success = True
        else:
            msg = 'No sensors are registered with this account'
    else:
        msg = 'Please contact support@thermocloud.net - User is not tied to an account'

    return render(request, "home/dashboard.html", {"sensor_list":sensor_list, "msg": msg, "success": success})
    

@login_required(login_url="/login/")
def sensor_overview(request):
    msg = None
    success = False

    real_user = AuthUser.objects.get(id=request.user.id)
    try:
        auth_user_group = AuthUserGroups.objects.get(user=real_user)
        real_group = auth_user_group.group
    except AuthUserGroups.DoesNotExist:
        auth_user_group = None
        real_group = None
    if real_group:
        try:
            request_uuid = request.GET['uuid']
            sensor_object = Sensor.objects.get(uuid=request_uuid)
        except Sensor.DoesNotExist:
            sensor_object = None
        if sensor_object:
            try:
                result = AuthSensorGroups.objects.get(sensor=sensor_object, group=real_group)
            except AuthSensorGroups.DoesNotExist:
                result = None
            if result:
                timespan_days = 7
                if request.GET.get('timespan'):
                    timespan_days = int(request.GET.get('timespan'))
                last_timespan_days = datetime.now() - timedelta(days=timespan_days)

                sensor_raw_data = SensorData.objects.filter(sensor=sensor_object, created__gt=last_timespan_days)
                sensor_raw_time_data = list(sensor_raw_data.values_list('created', flat=True))
                sensor_temperature_data = list(sensor_raw_data.values_list('temperature_f', flat=True))
                sensor_time_data = [date_obj.strftime("%b %d, %Y %r") for date_obj in sensor_raw_time_data]
                sensor_info = sensor_object
                sensor_info.timespan = str(timespan_days)
                success = True
            else:
                msg = 'This sensor does not belong to your account'
        else:
            msg = 'This sensor does not exist'
    else:
        msg = 'Please contact support@thermocloud.net - User is not tied to an account'

    return render(request, "home/sensor_overview.html", {"sensor_time_data":sensor_time_data, "sensor_temperature_data":sensor_temperature_data, "sensor_info":sensor_info, "msg": msg, "success": success})