from django import forms
from  rules_fetcher_display.models import prerouting,postrouting

class preform(forms.Form):
    #for custom validations like this field should have this many character and validatos like so
    routing = forms.CharField(max_length=20)
    source_ip = forms.CharField(max_length=18)
    source_port = forms.CharField(max_length=19)
    protocol = forms.CharField(max_length=10)
    destination_ip = forms.CharField(max_length=18)
    destination_port = forms.CharField(max_length=10)
class postform(forms.Form):
    routing = forms.CharField(max_length=20)
    source_ip = forms.CharField(max_length=18)
    destination_ip = forms.CharField(max_length=18)


