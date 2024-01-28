from django.db import models

# Create your models here.
class BookData(models.Model):
    uid = models.PositiveIntegerField()
    year = models.PositiveIntegerField(unique=True)
    readingstats = models.JSONField(default = dict)

    class Meta:
        unique_together = ('uid', 'year')