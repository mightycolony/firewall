from django.shortcuts import render
from django.http import HttpResponse
from rules_adding import forms 
from rules_fetcher_display.models import prerouting,postrouting
from django.shortcuts import redirect
import sys
sys.path.append("python_scripts")

from python_scripts.sshcall import SSH

server_ip="10.62.32.234"
user_name="root"
password="wZby5y5GBZy5y1y5y5"

connection_call=SSH()
def tables_gen_pre(sourceip,sourceport,protocol,destinationip,destinationport):
    tables="iptables -t nat -A PREROUTING -d {} -p {} -m {} --dport {} -j DNAT --to-destination {}:{}".format(sourceip,protocol,protocol,sourceport,destinationip,destinationport)
    return tables
 
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
                   server_data.append(form.cleaned_data['protocol'])
                   server_data.append(form.cleaned_data['destination_ip'])
                   server_data.append(form.cleaned_data['destination_port'])
    
    
                   cmd=tables_gen_pre(server_data[0],server_data[1],server_data[2],server_data[3],server_data[4])
                   print(cmd)
                   connection_call.ssh_call(server_ip,user_name,password,cmd)
   

               elif routing == "postrouting":
                  print(routing)
                  postrouting.objects.get_or_create(source_ip=data['destination_ip'], destination_ip=data['source_ip'], routing=data['routing'])
               elif routing == "both":
                  print(routing)
                  prerouting.objects.get_or_create(**data)
                  postrouting.objects.get_or_create(source_ip=data['destination_ip'], destination_ip=data['source_ip'], routing=data['routing'])
               
   return redirect('rules')








#connection_call.ssh_call()
