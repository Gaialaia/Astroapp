from django.db import models

from django.forms import DateTimeInput
from django.utils import timezone
from datetime import datetime as dt

# Create your models here.

now = dt.now()
class Chart(models.Model):

    objects = None

    chart_date = models.DateTimeField(default=now)
    city = models.CharField(default='Ufa')
    country = models.CharField(default='Russia')

    def __str__(self):
        return f'{self.chart_date}, {self.city}, {self.country}'

class TransitChart(models.Model):
    objects = None

    event_date = models.DateTimeField(default=now, help_text='Birth, holiday, marriage etc')
    event_city = models.CharField(default='Ufa')
    event_country = models.CharField(default='Russia')

    transit_date = models.DateTimeField(default=None)
    transit_city = models.CharField(default=None)
    transit_country = models.CharField(default=None)

    def __str__(self):
        return (f'{self.event_date}, {self.event_city}, {self.event_country}'
                f'{self.transit_date},{self.transit_city},  {self.transit_country}')


