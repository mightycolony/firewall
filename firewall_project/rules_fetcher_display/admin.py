from django.contrib import admin
from rules_fetcher_display.models import prerouting,postrouting
# Register your models here.


admin.site.register(prerouting)
admin.site.register(postrouting)