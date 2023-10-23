from rules_fetcher_display.models import prerouting,postrouting
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404

from django.http import HttpResponse

def delete_object(request, object_id):
    print(object_id)
    try:
        obj = get_object_or_404(postrouting, id=object_id)
        obj.delete()
        return redirect('rules')    
    except postrouting.DoesNotExist:
        return HttpResponse("Object not found")


