from django.shortcuts import render
from django.http import HttpResponse
from rules_adding import forms 
from rules_fetcher_display.models import prerouting,postrouting
from django.shortcuts import redirect

# Create your views here.
def add(request):
   form = forms.addform()

   if request.method == "POST":
      form = forms.addform(request.POST) 
      if form.is_valid():
               data = form.cleaned_data
               routing=data['routing']
               print(routing)
               if routing == "prerouting":   
                   print(routing)
                   prerouting.objects.get_or_create(**data)
               elif routing == "postrouting":
                  print(routing)
                  postrouting.objects.get_or_create(source_ip=data['destination_ip'], destination_ip=data['source_ip'], routing=data['routing'])
               elif routing == "both":
                  print(routing)
                  prerouting.objects.get_or_create(**data)
                  postrouting.objects.get_or_create(source_ip=data['destination_ip'], destination_ip=data['source_ip'], routing=data['routing'])
               
   return redirect('rules')
