from rules_fetcher_display.models import prerouting,postrouting,ServerDetails

from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
import json

from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required


from z_python_scripts.ip_add_delete import del_pol,save_pol

from rules_fetcher_display.models import prerouting,postrouting,ServerDetails
from rules_adding.models import LastPK
from django.db.models import Max





def tables_gen_delete(routing,sourceip=None,sourceport=None,protocol=None,destinationip=None,destinationport=None,policy_id=None):
    if routing == "preroute":
        tables="iptables -t nat -D PREROUTING -m comment --comment policy-{} -d {} -p {} -m {} --dport {} -j DNAT --to-destination {}:{}".format(policy_id,sourceip,protocol,protocol,sourceport,destinationip,destinationport)
        return tables
    elif routing == "postroute":
        tables="iptables -t nat -D POSTROUTING -m comment --comment policy-{} -d {} -j SNAT --to-source {}".format(policy_id,destinationip,sourceip)
        return tables

def tables_gen_save(routing,sourceip=None,sourceport=None,protocol=None,destinationip=None,destinationport=None):
    if routing == "prerouting":
        tables="iptables -t nat -R PREROUTING -d {} -p {} -m {} --dport {} -j DNAT --to-destination {}:{}".format(sourceip,protocol,protocol,sourceport,destinationip,destinationport)
        
        return tables
    elif routing == "postrouting":
        tables="iptables -t nat -R POSTROUTING -d {} -j SNAT --to-source {}".format(destinationip,sourceip)
        return tables





serv=ServerDetails.objects.get(pk=1)

@never_cache
@login_required
@permission_required('rules_fetcher_display.edit')
def delete_object(request, object_id,types):
  
    try:
        if types == "preroute":
             pre_policy_id=object_id
             print(pre_policy_id)

             obj = get_object_or_404(prerouting, id=object_id)
             
             cmd=tables_gen_delete(types,obj.source_ip,obj.source_port,obj.protocol,obj.destination_ip,obj.destination_port,policy_id=pre_policy_id)
             print("cmd",cmd)
             error_both_pre=del_pol(types,serv.ip,serv.username,"notu",cmd,policy_id=object_id,sourceip=obj.source_ip)
             #print(error_both_pre)
             obj.delete()
             
        elif types == "postroute":
             post_policy_id=object_id
             print(post_policy_id)
             obj1 = get_object_or_404(postrouting, id=object_id)
             cmd1=tables_gen_delete(types,destinationip=obj1.source_ip,sourceip=obj1.destination_ip,policy_id=post_policy_id)
             print(cmd1)
             error_both_post=del_pol(types,serv.ip,serv.username,"notu",cmd1,policy_id=object_id)
             print(error_both_post)
             obj1.delete()
             
        return redirect('rules')    
    except (prerouting.DoesNotExist,postrouting.DoesNotExist):
        return HttpResponse("Object not found")




@never_cache
@login_required
@permission_required('rules_fetcher_display.edit')
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
            sav_err_pre=save_pol(routing,serv.ip,serv.username,"notu",cmd1,policy_id=saved_id,sourceip=data_post[1],destinationip=data_post[0])
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
            sav_err_ppost=save_pol(routing,serv.ip,serv.username,"notu",cmd,policy_id=saved_id,sourceip=data_pre[0],destinationip=data_pre[3],sourceport=data_pre[1],destinationport=data_pre[4])
            print(sav_err_ppost)
            instance_pre.save()
        return HttpResponse("Data saved successfully")

        

