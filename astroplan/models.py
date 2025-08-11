from django.db import models

from django.forms import DateTimeInput

from django.utils import timezone
from datetime import datetime as dt

# Create your models here.

now = dt.now()
class Chart(models.Model):

    objects = None

    chart_date = models.DateTimeField(default=timezone.now)
    city = models.CharField(default='Ufa')
    country = models.CharField(default='Russia')

    def __str__(self):
        return f'{self.chart_date}, {self.city}, {self.country}'



class TransitChart(models.Model):
    objects = None

    event_date = models.DateTimeField(default=timezone.now)
    event_city = models.CharField(default='Ufa')
    event_country = models.CharField(default='Russia')

    transit_date = models.DateTimeField(default=timezone.now)
    transit_city = models.CharField(default=None)
    transit_country = models.CharField(default=None)

    def __str__(self):
        return (f'{self.event_date}, {self.event_city}, {self.event_country}'
                f'{self.transit_date},{self.transit_city},  {self.transit_country}')


class ZodiacInColors(models.Model):

    chart_date = models.DateTimeField(default=timezone.now)
    chart_city = models.CharField(default='Ufa')
    chart_country = models.CharField(default='Russia')

    track_aries_axis_fc = models.CharField(max_length=20, default='#A800D8')
    track_aries_axis_ec = models.CharField(max_length=20, default='aliceblue')
    track_aries_axis_tc = models.CharField(max_length=20,  default='#2BC200')

    track_leo_axis_fc = models.CharField(max_length=20, default='#A800D8')
    track_leo_axis_ec = models.CharField(max_length=20, default='aliceblue')
    track_leo_axis_tc = models.CharField(max_length=20, default='#2BC200')

    track_sag_axis_fc = models.CharField(max_length=20, default='#A800D8')
    track_sag_axis_ec = models.CharField(max_length=20, default='aliceblue')
    track_sag_axis_tc = models.CharField(max_length=20, default='#2BC200')

    track_aqua_axis_fc = models.CharField(max_length=20, default='#A800D8')
    track_aqua_axis_ec = models.CharField(max_length=20, default='aliceblue')
    track_aqua_axis_tc = models.CharField(max_length=20, default='hotpink')

    track_gemini_axis_fc = models.CharField(max_length=20, default='#A800D8')
    track_gemini_axis_ec = models.CharField(max_length=20, default='aliceblue')
    track_gemini_axis_tc = models.CharField(max_length=20,  default='#2BC200')

    track_libra_axis_fc = models.CharField(max_length=20,default='#A800D8')
    track_libra_axis_ec = models.CharField(max_length=20, default='aliceblue')
    track_libra_axis_tc = models.CharField(max_length=20, default='#2BC200')

    track_scorpio_axis_fc = models.CharField(max_length=20,default='#A800D8' )
    track_scorpio_axis_ec = models.CharField(max_length=20, default='aliceblue')
    track_scorpio_axis_tc = models.CharField(max_length=20, default='#2BC200')

    track_cancer_axis_fc = models.CharField(max_length=20,default='#A800D8')
    track_cancer_axis_ec = models.CharField(max_length=20, default='aliceblue')
    track_cancer_axis_tc = models.CharField(max_length=20, default='#2BC200')

    track_pisces_axis_fc = models.CharField(max_length=20, default='#A800D8')
    track_pisces_axis_ec = models.CharField(max_length=20, default='aliceblue')
    track_pisces_axis_tc = models.CharField(max_length=20, default='#2BC200')

    track_taurus_axis_fc = models.CharField(max_length=20, default='#A800D8')
    track_taurus_axis_ec = models.CharField(max_length=20, default='aliceblue')
    track_taurus_axis_tc = models.CharField(max_length=20,  default='#2BC200')

    track_virgo_axis_fc = models.CharField(max_length=20, default='#A800D8')
    track_virgo_axis_ec = models.CharField(max_length=20, default='aliceblue')
    track_virgo_axis_tc = models.CharField(max_length=20, default='#2BC200')

    track_capricorn_axis_fc = models.CharField(max_length=20, default='#A800D8')
    track_capricorn_axis_ec = models.CharField(max_length=20, default='aliceblue')
    track_capricorn_axis_tc = models.CharField(max_length=20, default='#2BC200')

    degrees_track_ec = models.CharField(max_length=20, default='aliceblue')
    degrees_ticks_color = models.CharField(max_length=20,default='aliceblue')

    sun_symbol_c = models. CharField(max_length=20, default='aliceblue')
    sun_symbol_s = models.IntegerField(default=7)
    sun_marker_c = models.CharField(max_length=20, default='gold')

    moon_symbol_c = models.CharField(max_length=20,  default='aliceblue')
    moon_symbol_s = models.IntegerField(default=8)
    moon_marker_c = models.CharField(max_length=20, default='aliceblue')

    mercury_symbol_c = models.CharField(max_length=20, default='aliceblue')
    mercury_symbol_s = models.IntegerField(default=5)
    mercury_marker_c = models.CharField(max_length=20, default='grey')

    venus_symbol_c = models.CharField(max_length=20, default='aliceblue')
    venus_symbol_s = models.IntegerField(default=9)
    venus_marker_c = models.CharField(max_length=20, default='pink')

    mars_symbol_c = models.CharField(max_length=20,  default='aliceblue')
    mars_symbol_s = models.IntegerField(default=6)
    mars_marker_c = models.CharField(max_length=20, default='red')

    jupiter_symbol_c = models.CharField(max_length=20, default='aliceblue')
    jup_symbol_s = models.IntegerField(default=12)
    jup_marker_c = models.CharField(max_length=20, default='royalblue')

    saturn_symbol_c = models.CharField(max_length=20, default='aliceblue')
    saturn_symbol_s = models.IntegerField(default=10)
    saturn_marker_c = models.CharField(max_length=20, default='darkslateblue')

    uranus_symbol_c = models.CharField(max_length=20, default='aliceblue')
    uranus_symbol_s = models.IntegerField(default=13)
    uranus_marker_c = models.CharField(max_length=20, default='chartreuse')

    neptune_symbol_c = models.CharField(max_length=20,  default='aliceblue')
    neptune_symbol_s = models.IntegerField(default=13)
    neptune_marker_c = models.CharField(max_length=20, default='darkcyan' )

    pluto_symbol_c = models.CharField(max_length=20, default='aliceblue')
    pluto_symbol_s = models.IntegerField(default=13)
    pluto_marker_c = models.CharField(max_length=20, default='firebrick')
    
    
    def __str__(self):
        return (f'{self.chart_date}, {self.chart_city}, {self.chart_country}'
                f'{self.track_aries_axis_ec},{self.track_aries_axis_tc},{self.track_aries_axis_tc}'
                f'{self.track_leo_axis_ec},{self.track_leo_axis_tc},{self.track_leo_axis_tc}'
                f'{self.track_sag_axis_ec},{self.track_sag_axis_tc},{self.track_sag_axis_tc}'
                f'{self.track_aqua_axis_ec},{self.track_aqua_axis_tc},{self.track_aqua_axis_tc}'
                f'{self.track_gemini_axis_ec},{self.track_gemini_axis_tc},{self.track_gemini_axis_tc}'
                f'{self.track_libra_axis_ec},{self.track_libra_axis_tc},{self.track_libra_axis_tc}'
                f'{self.track_virgo_axis_ec},{self.track_virgo_axis_tc},{self.track_virgo_axis_tc}'
                f'{self.track_taurus_axis_ec},{self.track_taurus_axis_tc},{self.track_taurus_axis_tc}'
                f'{self.track_capricorn_axis_ec},{self.track_capricorn_axis_tc},{self.track_capricorn_axis_tc}'
                f'{self.track_scorpio_axis_ec},{self.track_scorpio_axis_tc},{self.track_scorpio_axis_tc}'
                f'{self.track_cancer_axis_ec},{self.track_cancer_axis_tc},{self.track_cancer_axis_tc}'
                f'{self.track_pisces_axis_ec},{self.track_pisces_axis_tc},{self.track_pisces_axis_tc}'
                f'{self.sun_marker_c}, {self.sun_symbol_c},{self.sun_symbol_s}'
                f'{self.moon_marker_c}, {self.moon_symbol_c},{self.moon_symbol_s}'
                f'{self.mercury_marker_c}, {self.mercury_symbol_c},{self.mercury_symbol_s}'
                f'{self.venus_marker_c}, {self.venus_symbol_c},{self.venus_symbol_s}'
                f'{self.mars_marker_c}, {self.mars_symbol_c},{self.mars_symbol_s}'
                f'{self.jup_marker_c}, {self.jupiter_symbol_c},{self.jup_symbol_s}'
                f'{self.saturn_marker_c}, {self.saturn_symbol_c},{self.saturn_symbol_s}'
                f'{self.uranus_marker_c}, {self.uranus_symbol_c},{self.uranus_symbol_s}'
                f'{self.neptune_marker_c}, {self.neptune_symbol_c},{self.neptune_symbol_s}'
                f'{self.pluto_marker_c}, {self.pluto_symbol_c},{self.pluto_symbol_s}'
                f'{self.degrees_ticks_color}, {self.degrees_track_ec}')

