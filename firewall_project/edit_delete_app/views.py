from rules_fetcher_display.models import prerouting,postrouting
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
import json
import sys
sys.path.append("python_scripts")

def tables_gen_delete(routing,sourceip,sourceport=None,protocol=None,destinationip=None,destinationport=None):
    if routing == "preroute":
        tables="iptables -t nat -D PREROUTING -d {} -p {} -m {} --dport {} -j DNAT --to-destination {}:{}".format(sourceip,protocol,protocol,sourceport,destinationip,destinationport)
        return tables
    elif routing == "postroute":
        tables="iptables -t nat -D POSTROUTING -d {} -j SNAT --to-source {}".format(destinationip,sourceip)
        return tables

def tables_gen_save(routing,sourceip,sourceport=None,protocol=None,destinationip=None,destinationport=None):
    if routing == "prerouting":
        tables="iptables -t nat -R PREROUTING -d {} -p {} -m {} --dport {} -j DNAT --to-destination {}:{}".format(sourceip,protocol,protocol,sourceport,destinationip,destinationport)
        return tables
    elif routing == "postrouting":
        tables="iptables -t nat -R POSTROUTING -d {} -j SNAT --to-source {}".format(destinationip,sourceip)
        return tables



def delete_object(request, object_id,types):
    try:
        if types == "preroute":
             obj = get_object_or_404(prerouting, id=object_id)
             cmd=tables_gen_delete(types,obj.source_ip,obj.source_port,obj.protocol,obj.destination_ip,obj.destination_port)
             print(cmd)
             obj.delete()
        elif types == "postroute":
             obj1 = get_object_or_404(postrouting, id=object_id)
             cmd1=tables_gen_delete(types,destinationip=obj1.destination_ip,sourceip=obj1.source_ip)
             print(cmd1)
             obj1.delete()
        return redirect('rules')    
    except (prerouting.DoesNotExist,postrouting.DoesNotExist):
        return HttpResponse("Object not found")





def save_object_post(request,routing,saved_id):
    if routing == "postrouting":
        try:
            instance_post = postrouting.objects.get(id=saved_id)  
            print(instance_post)
        except instance_post.DoesNotExist:
          pass

        if instance_post:
            data_post = json.loads(request.body)
            instance_post.source_ip=data_post[0]
            instance_post.destination_ip=data_post[1] 
            cmd1=tables_gen_save(routing,destinationip=data_post[0],sourceip=data_post[1])
            print(cmd1)
            instance_post.save()
        return HttpResponse("Data saved successfully")
    elif routing == "prerouting":

        try:
            instance_pre = prerouting.objects.get(id=saved_id)  
            print(instance_pre)
        except instance_pre.DoesNotExist:
            pass

        if instance_pre:
            data_pre = json.loads(request.body)
            instance_pre.source_ip=data_pre[0]
            instance_pre.source_port=data_pre[1]
            instance_pre.protocol=data_pre[2]
            instance_pre.destination_ip=data_pre[3] 
            instance_pre.destination_port=data_pre[4]
            cmd=tables_gen_save(routing,data_pre[0],data_pre[1],data_pre[2],data_pre[3],data_pre[4])
            print(cmd)
            instance_pre.save()
        return HttpResponse("Data saved successfully")

        
