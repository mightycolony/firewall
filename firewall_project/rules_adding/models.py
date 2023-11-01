from django.db import models
from rules_fetcher_display.models import prerouting,postrouting
# Create your models here.

from django.db import models

class LastPK(models.Model):
    prerouting_last_pk = models.PositiveIntegerField(default=0)
    postrouting_last_pk = models.PositiveIntegerField(default=0)

    # Ensuring that there is only one instance of the LastPK model
    def save(self, *args, **kwargs):
        self.pk = 1
        super(LastPK, self).save(*args, **kwargs)