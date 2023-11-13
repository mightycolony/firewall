from django import forms
from  rules_fetcher_display.models import prerouting,postrouting
from django.http import HttpResponse
from django.core.exceptions import ValidationError
from django.core.validators import validate_ipv4_address




def validate_ip_address(value):
    try:
        validate_ipv4_address(value)
    except ValidationError:
           return "Enter a valid IPv4 address."
    

class preform(forms.Form):
    #for custom validations like this field should have this many character and validatos like so
    routing = forms.CharField(max_length=20)
    source_ip = forms.CharField(max_length=15)
    source_port = forms.CharField(max_length=19)
    protocol = forms.CharField(max_length=10)
    destination_ip = forms.CharField(max_length=15)
    destination_port = forms.CharField(max_length=10)
class postform(forms.Form):
    routing = forms.CharField(max_length=20)
    source_ip = forms.CharField(max_length=18,validators=[validate_ip_address])
    destination_ip = forms.CharField(max_length=18)




