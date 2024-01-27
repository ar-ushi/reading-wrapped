from django.db import models
from django.forms import JSONField

# Create your models here.
class BookData(models.Model):
    uid = models.PositiveIntegerField()
    year = models.PositiveIntegerField(unique=True)
    yearlystats = JSONField()

    class Meta:
        unique_together = ('userid', 'year')
    