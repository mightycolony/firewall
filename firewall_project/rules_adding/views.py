from django.shortcuts import render
from django.http import HttpResponse
from rules_adding import forms 
from rules_fetcher_display.models import prerouting,postrouting
from django.shortcuts import redirect
import sys
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required



def tables_gen_add(routing,sourceip,sourceport=None,protocol=None,destinationip=None,destinationport=None):
    if routing == "prerouting":
        tables="iptables -t nat -A PREROUTING -d {} -p {} -m {} --dport {} -j DNAT --to-destination {}:{}".format(sourceip,protocol,protocol,sourceport,destinationip,destinationport)
        return tables
    elif routing == "postrouting":
        tables="iptables -t nat -A POSTROUTING -d {} -j SNAT --to-source {}".format(destinationip,sourceip)
        return tables
    elif routing == "both":
        tables="iptables -t nat -A PREROUTING -d {} -p {} -m {} --dport {} -j DNAT --to-destination {}:{}".format(sourceip,protocol,protocol,sourceport,destinationip,destinationport)
        tables2="iptables -t nat -A POSTROUTING -d {} -j SNAT --to-source {}".format(destinationip,sourceip)
        return tables,tables2

# Create your views here.
@never_cache
@login_required
@permission_required('rules_fetcher_display.edit')
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
               server_data2=[]
               data = form.cleaned_data
               routing=data['routing']
               if routing == "prerouting":   
                   prerouting.objects.get_or_create(**data)
                   server_data.extend([
                        form.cleaned_data['routing'],
                        form.cleaned_data['source_ip'],
                        form.cleaned_data['source_port'],
                        form.cleaned_data['protocol'],
                        form.cleaned_data['destination_ip'],
                        form.cleaned_data['destination_port']
                        ])
                   cmd=tables_gen_add(routing=server_data[0],sourceip=server_data[1],sourceport=server_data[2],protocol=server_data[3],destinationip=server_data[4],destinationport=server_data[5])
                   print(cmd)
                   #connection_call.ssh_call(server_ip,user_name,password,cmd)


               elif routing == "postrouting":
                   postrouting.objects.get_or_create(source_ip=data['destination_ip'], destination_ip=data['source_ip'], routing=data['routing'])
                   server_data.extend([
                        form.cleaned_data['routing'],
                        form.cleaned_data['source_ip'],
                        form.cleaned_data['destination_ip']
                        ])
                   cmd=tables_gen_add(routing=server_data[0],sourceip=server_data[1],destinationip=server_data[2])
                   print(cmd)
               elif routing == "both":
                  print(routing)
                  prerouting.objects.get_or_create(**data)
                  server_data.extend([
                        form.cleaned_data['routing'],
                        form.cleaned_data['source_ip'],
                        form.cleaned_data['source_port'],
                        form.cleaned_data['protocol'],
                        form.cleaned_data['destination_ip'],
                        form.cleaned_data['destination_port']
                        ])
                  postrouting.objects.get_or_create(source_ip=data['destination_ip'], destination_ip=data['source_ip'], routing=data['routing'])
                  server_data2.extend([
                        form.cleaned_data['routing'],
                        form.cleaned_data['source_ip'],
                        form.cleaned_data['destination_ip']
                        ])
                  cmd,cmd2 = tables_gen_add(routing=server_data[0],sourceip=server_data[1],sourceport=server_data[2],protocol=server_data[3],destinationip=server_data[4],destinationport=server_data[5])
               

                  print(cmd)
                  print(cmd2)
               
   return redirect('rules')








