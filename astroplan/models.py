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

    event_date = models.DateTimeField(default=now)
    event_city = models.CharField(default='Ufa')
    event_country = models.CharField(default='Russia')

    transit_date = models.DateTimeField(default=None)
    transit_city = models.CharField(default=None)
    transit_country = models.CharField(default=None)

    def __str__(self):
        return (f'{self.event_date}, {self.event_city}, {self.event_country}'
                f'{self.transit_date},{self.transit_city},  {self.transit_country}')


class ZodiacInColors(models.Model):

    chart_date = models.DateTimeField(default=None)
    chart_city = models.CharField()
    chart_country = models.CharField()

    track_aries_axis_fc = models.CharField(max_length=20)
    track_aries_axis_ec = models.CharField(max_length=20)
    track_aries_axis_tc = models.CharField(max_length=20)

    track_leo_axis_fc = models.CharField(max_length=20)
    track_leo_axis_ec = models.CharField(max_length=20)
    track_leo_axis_tc = models.CharField(max_length=20)

    track_sag_axis_fc = models.CharField(max_length=20)
    track_sag_axis_ec = models.CharField(max_length=20)
    track_sag_axis_tc = models.CharField(max_length=20)

    track_aqua_axis_fc = models.CharField(max_length=20)
    track_aqua_axis_ec = models.CharField(max_length=20)
    track_aqua_axis_tc = models.CharField(max_length=20)

    track_gemini_axis_fc = models.CharField(max_length=20)
    track_gemini_axis_ec = models.CharField(max_length=20)
    track_gemini_axis_tc = models.CharField(max_length=20)

    track_libra_axis_fc = models.CharField(max_length=20)
    track_libra_axis_ec = models.CharField(max_length=20)
    track_libra_axis_tc = models.CharField(max_length=20)

    track_scorpio_axis_fc = models.CharField(max_length=20)
    track_scorpio_axis_ec = models.CharField(max_length=20)
    track_scorpio_axis_tc = models.CharField(max_length=20)

    track_cancer_axis_fc = models.CharField(max_length=20)
    track_cancer_axis_ec = models.CharField(max_length=20)
    track_cancer_axis_tc = models.CharField(max_length=20)

    track_pisces_axis_fc = models.CharField(max_length=20)
    track_pisces_axis_ec = models.CharField(max_length=20)
    track_pisces_axis_tc = models.CharField(max_length=20)

    track_taurus_axis_fc = models.CharField(max_length=20)
    track_taurus_axis_ec = models.CharField(max_length=20)
    track_taurus_axis_tc = models.CharField(max_length=20)

    track_virgo_axis_fc = models.CharField(max_length=20)
    track_virgo_axis_ec = models.CharField(max_length=20)
    track_virgo_axis_tc = models.CharField(max_length=20)

    track_capricorn_axis_fc = models.CharField(max_length=20)
    track_capricorn_axis_ec = models.CharField(max_length=20)
    track_capricorn_axis_tc = models.CharField(max_length=20)

    degrees_track_ec = models.CharField(max_length=20)
    degrees_ticks_color = models.CharField(max_length=20)

    sun_symbol_c = models. CharField(max_length=20)
    sun_symbol_s = models.IntegerField()
    sun_marker_c = models.CharField(max_length=20)

    moon_symbol_c = models.CharField(max_length=20)
    moon_symbol_s = models.IntegerField()
    moon_marker_c = models.CharField(max_length=20)

    mercury_symbol_c = models.CharField(max_length=20)
    mercury_symbol_s = models.IntegerField()
    mercury_marker_c = models.CharField(max_length=20 )

    venus_symbol_c = models.CharField(max_length=20)
    venus_symbol_s = models.IntegerField()
    venus_marker_c = models.CharField(max_length=20)

    mars_symbol_c = models.CharField(max_length=20 )
    mars_symbol_s = models.IntegerField()
    mars_marker_c = models.CharField(max_length=20)

    jupiter_symbol_c = models.CharField(max_length=20)
    jup_symbol_s = models.IntegerField()
    jup_marker_c = models.CharField(max_length=20)

    saturn_symbol_c = models.CharField(max_length=20)
    saturn_symbol_s = models.IntegerField()
    saturn_marker_c = models.CharField(max_length=20)

    uranus_symbol_c = models.CharField(max_length=20)
    uranus_symbol_s = models.IntegerField()
    uranus_marker_c = models.CharField(max_length=20)

    neptune_symbol_c = models.CharField(max_length=20 )
    neptune_symbol_s = models.IntegerField()
    neptune_marker_c = models.CharField(max_length=20 )

    pluto_symbol_c = models.CharField(max_length=20)
    pluto_symbol_s = models.IntegerField()
    pluto_marker_c = models.CharField(max_length=20)
    
    
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

