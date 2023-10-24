from rules_fetcher_display.models import prerouting,postrouting
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
import json

def delete_object(request, object_id,types):
    print(object_id)
    print(types)
    try:
        if types == "preroute":
             obj = get_object_or_404(prerouting, id=object_id)
             obj.delete()
        elif types == "postroute":
             obj1 = get_object_or_404(postrouting, id=object_id)
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
            

            instance_pre.save()
        return HttpResponse("Data saved successfully")

        
