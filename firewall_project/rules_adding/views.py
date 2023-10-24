from django.shortcuts import render
from django.http import HttpResponse
from rules_adding import forms 
from rules_fetcher_display.models import prerouting,postrouting
from django.shortcuts import redirect
from .sshcall import SSH 
# Create your views here.
def add(request):

   if request.method == "POST":
      routing = request.POST.get('routing')

      if routing == "prerouting": 
        form = forms.preform(request.POST) 
      elif routing == "postrouting":
          form = forms.postform(request.POST)
      else:
          form = forms.preform(request.POST)

      if form.is_valid():
               server_data=[]
               data = form.cleaned_data
               routing=data['routing']
               if routing == "prerouting":   
                   prerouting.objects.get_or_create(**data)
                   server_data.append(form.cleaned_data['source_ip'])
                   server_data.append(form.cleaned_data['source_port'])
                   server_data.form.cleaned_data(['protocol'])
                   server_data.form.cleaned_data(['destination_ip'])
                   server_data.form.cleaned_data(['destination_port'])
                   print(server_data)
               elif routing == "postrouting":
                  print(routing)
                  postrouting.objects.get_or_create(source_ip=data['destination_ip'], destination_ip=data['source_ip'], routing=data['routing'])
               elif routing == "both":
                  print(routing)
                  prerouting.objects.get_or_create(**data)
                  postrouting.objects.get_or_create(source_ip=data['destination_ip'], destination_ip=data['source_ip'], routing=data['routing'])
               
   return redirect('rules')





connection_call=SSH()
#connection_call.ssh_call()
