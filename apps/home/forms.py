# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import forms


class RegisterSensor(forms.Form):
    mac = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Mac Address",
                "class": "form-control"
            }
        ))
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Sensor Nickname",
                "class": "form-control"
            }
        ))

#    class Meta:
#        model = User
#        fields = ('username', 'email', 'account', 'password1', 'password2')
