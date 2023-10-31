from django.shortcuts import render
from django.http import HttpResponse
from rules_adding import forms 
from rules_fetcher_display.models import prerouting,postrouting
from django.shortcuts import redirect
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required
from z_python_scripts.ip_add_delete import ip_add
from django.contrib import messages

#from z_python_scripts import ip_add_delete

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




previous_object_pre = prerouting.objects.order_by('-id').first()
previous_object_id_pre = previous_object_pre.id if previous_object_pre else None

previous_object_post = postrouting.objects.order_by('-id').first()
previous_object_id_post = previous_object_post.id if previous_object_post else None


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
                   policyid=previous_object_id_pre +1
                   error_pre=ip_add(routing,"10.0.2.15","root","notu",policyid,cmd)
                   print(error_pre[1])
                   if error_pre[1] != 0:
                        print("returned error: {} with error code: {}".format(error_pre[0].strip("\n"), error_pre[1]))
                        error_msg="returned error: {} with error code: {}".format(error_pre[0].strip("\n"), error_pre[1])
                        request.session['error_msg'] = error_msg
                    

               elif routing == "postrouting":
                   postrouting.objects.get_or_create(source_ip=data['destination_ip'], destination_ip=data['source_ip'], routing=data['routing'])
                   server_data.extend([
                        form.cleaned_data['routing'],
                        form.cleaned_data['source_ip'],
                        form.cleaned_data['destination_ip']
                        ])
                   cmd2=tables_gen_add(routing=server_data[0],sourceip=server_data[1],destinationip=server_data[2])
                   policyid=previous_object_id_post +1
                   ip_add(routing,"10.0.2.15","root","notu",policyid,cmd2)
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
                  policyid=previous_object_id_pre +1
                  policyid=previous_object_id_post +1
                  ip_add(routing,"10.0.2.15","root","notu",policyid,cmd)

                  print(cmd)
                  print(cmd2)
               
   return redirect('rules')








