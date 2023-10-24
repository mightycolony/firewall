"""
URL configuration for firewall_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from rules_fetcher_display.views import combined_rules
from rules_adding.views import add
from edit_delete_app.views import delete_object,save_object_post


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', combined_rules,name='rules'),
    path('add/', add,name='adding'),
    path('delete/<str:types>/<int:object_id>/',delete_object,name='delete_object'),
    path('save/<str:routing>/<int:saved_id>/',save_object_post,name='save_object_post'),
    
]
