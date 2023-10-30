from django.shortcuts import render
from django.http import HttpResponse
from rules_fetcher_display.models import prerouting,postrouting
from rules_fetcher_display.forms import UserForm
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from z_python_scripts.custom_decorators import or_permission_required


# Create your views here.



#custom decorator for user - ro and rw

def pre_rules(request):
    pre = prerouting.objects.all()
    context = {'prerouting_data': pre}
    return context
def post_rules(request):
    post = postrouting.objects.all()
    context = {'postrouting_data': post}
    return context

@login_required
@or_permission_required('rules_fetcher_display.edit', 'rules_fetcher_display.view')
def combined_rules(request):

    pre_context = pre_rules(request)
    post_context = post_rules(request)

    if request.user.is_authenticated:
        user_group = request.user.groups.first()
    else:
        user_group = None

    # Merge the two context dictionaries into a single dictionary
    combined_context = {**pre_context, **post_context,'user_group': user_group}
    return render(request, 'index.html', combined_context)




@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('user_login'))



def user_login(request):
    
    if request.method ==  "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username,password=password)

        if user:
            if user.is_active:
                login(request,user) 
                if request.user.is_authenticated:
                        user_group = request.user.groups.first()
                        user_name = {'user_group': user_group}
                return HttpResponseRedirect(reverse('rules')) 
            else:
               return HttpResponse("Account not active") 
        else:
            print("someone trying to login and failed")
            print("username:{} and password{}".format(username,password))
        return HttpResponse("invalid login details supplied")
    
    else:
        form = UserForm()
        return render(request,'login.html',{"form":form})