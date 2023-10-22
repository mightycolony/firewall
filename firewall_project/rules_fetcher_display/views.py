from django.shortcuts import render
from django.http import HttpResponse

from rules_fetcher_display.models import prerouting,postrouting
# Create your views here.
def pre_rules(request):
    pre = prerouting.objects.all()
    context = {'prerouting_data': pre}
    return context
def post_rules(request):
    post = postrouting.objects.all()
    context = {'postrouting_data': post}
    return context

def combined_rules(request):
    pre_context = pre_rules(request)
    post_context = post_rules(request)

    # Merge the two context dictionaries into a single dictionary
    combined_context = {**pre_context, **post_context}
    return render(request, 'index.html', combined_context)