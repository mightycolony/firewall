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


def save_object(request,saved_id):
    try:
        instance = postrouting.objects.get(id=saved_id)  
        print(instance)
    except instance.DoesNotExist:
     pass

    if instance:
        data = json.loads(request.body)
        instance.source_ip=data[0]
        instance.destination_ip = data[1] 
        instance.save()
    return HttpResponse("Data saved successfully")

        