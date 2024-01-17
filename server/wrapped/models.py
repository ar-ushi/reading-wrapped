from django.db import models
from django.forms import JSONField

# Create your models here.
class Year(models.Model):
    year = models.PositiveIntegerField(unique= True)

class BookData(models.Model):
    userid = models.PositiveIntegerField()
    year = models.ForeignKey(Year, on_delete= models.CASCADE)
    reading_wrapped = JSONField()

    class Meta:
        unique_together = ('userid', 'year')
    