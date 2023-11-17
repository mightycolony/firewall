from django import forms
from  rules_fetcher_display.models import prerouting,postrouting
from django.http import HttpResponse
from django.core.exceptions import ValidationError
from django.core.validators import validate_ipv4_address




def validate_ip_address(value):
    try:
        # Assuming validate_ipv4_address is imported from somewhere
        validate_ipv4_address(value)
    except ValidationError:
        raise forms.ValidationError("Enter a valid IPv4 address.")

def tcp_udp(value):
    if value != "tcp" and value != "udp":
        raise forms.ValidationError("Enter a valid protocol")

def port_validation(value):
    if value < 1 or value > 65535:
        raise forms.ValidationError("Not a valid port number")

class preform(forms.Form):
    #for custom validations like this field should have this many character and validatos like so
    routing = forms.CharField(max_length=20)
    source_ip = forms.CharField(max_length=15,validators=[validate_ip_address])
    source_port = forms.IntegerField(validators=[port_validation])
    protocol = forms.CharField(max_length=3,validators=[tcp_udp])
    destination_ip = forms.CharField(max_length=15,validators=[validate_ip_address])
    destination_port = forms.IntegerField(validators=[port_validation])
class postform(forms.Form):
    routing = forms.CharField(max_length=20)
    source_ip = forms.CharField(max_length=18,validators=[validate_ip_address])
    destination_ip = forms.CharField(max_length=18,validators=[validate_ip_address])




