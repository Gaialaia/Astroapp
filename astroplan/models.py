from django.db import models

from django.forms import DateTimeInput
from django.utils import timezone
from datetime import datetime as dt

# Create your models here.
class Chart(models.Model):

    # class Months(models.IntegerChoices):
    #
    #     JANUARY = 1
    #     FEBRUARY = 2
    #     MARCH = 3

    objects = None
    now = dt.now()



    chart_date = models.DateTimeField(default=now)
    city = models.CharField(default='Ufa')
    country = models.CharField(default='Russia')



    def __str__(self):
        return f'{self.chart_date}, {self.city}, {self.country}'



