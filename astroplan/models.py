from django.contrib.auth import get_user_model
from django.db import models

from django.forms import DateTimeInput

from django.utils import timezone
from datetime import datetime as dt


now = dt.now()


class Chart(models.Model):

    objects = None
    chart_date = models.DateTimeField(default=timezone.now)
    city = models.CharField(default='Ufa')
    country = models.CharField(default='Russia')

    def __str__(self):
        return f'{self.chart_date}, {self.city}, {self.country}'





class FullChart(models.Model):

    objects = None

    chart_name = models.CharField(default='My birthdate')
    chart_date = models.DateTimeField(default=timezone.now)

    city = models.CharField(default='Ufa')
    country = models.CharField(default='Russia')
    drawer = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, default=1)

    Sun_deg = models.CharField(default='5°05')
    Sun_sign = models.CharField(default='Aquarius')

    Moon_deg = models.CharField(default='14°44')
    Moon_sign = models.CharField(default='Taurus')

    Mercury_deg = models.CharField(default='18°04')
    Mercury_sign = models.CharField(default='Aquarius')

    Venus_deg = models.CharField(default='12°05')
    Venus_sign = models.CharField(default='Aquarius')

    Mars_deg = models.CharField(default='15°21')
    Mars_sign =  models.CharField(default='Scorpio')

    Jupiter_deg = models.CharField(default='5°37')
    Jupiter_sign = models.CharField(default='Aquarius')

    Saturn_deg = models.CharField(default='15°18')
    Saturn_sign = models.CharField(default='Scorpio')

    Uranus_deg = models.CharField(default='28°05')
    Uranus_sign = models.CharField(default='Scorpio')

    Neptune_deg = models.CharField(default='11°60')
    Neptune_sign = models.CharField(default='Sagittarius')

    Pluto_deg = models.CharField(default='13°40')
    Pluto_sign = models.CharField(default='Libra')

    first_house = models.CharField(default='Ascendant')
    asc_deg = models.CharField(default='0°')
    asc_sign = models.CharField(default='Aries')

    second_house = models.CharField(default='What you have with & in you')
    resource_deg = models.CharField(default='30°')
    resource_sign = models.CharField(default='Taurus')

    third_house = models.CharField(default='Mentality')
    mental_deg = models.CharField(default='60°')
    mental_sign = models.CharField(default='Gemini')

    forth_house = models.CharField(default='Home')
    home_deg = models.CharField(default='90°')
    home_sign = models.CharField(default='Crab')

    fifth_house = models.CharField(default='Games')
    game_deg = models.CharField(default='120°')
    game_sign = models.CharField(default='Crab')

    sixth_house = models.CharField(default='Work')
    work_deg = models.CharField(default='150°')
    work_sign = models.CharField(default='Virgo')

    seventh_house = models.CharField(default='Relationship')
    rel_deg = models.CharField(default='180°')
    rel_sign = models.CharField(default='Libra')

    eighth_house = models.CharField(default='Magic')
    magic_deg = models.CharField(default='210°')
    magic_sign = models.CharField(default='Scorpio')

    nineth_house = models.CharField(default='Esoteric knowledge')
    esoteric_deg = models.CharField(default='230°')
    esoteric_sign = models.CharField(default='Sagittarius')

    tenth_house = models.CharField(default='Status')
    status_deg = models.CharField(default='260°')
    status_sign = models.CharField(default='Capricorn')

    eleventh_house = models.CharField(default='Interests')
    interests_deg = models.CharField(default='290°')
    interests_sign = models.CharField(default='Aquarius')

    twelfth_house = models.CharField(default='Benefits')
    benefits_deg = models.CharField(default='330°')
    benefits_sign = models.CharField(default='Pisces')


    chart_image = models.ImageField(upload_to='chart_plots/')

    def __str__(self):
        return (f'{self.chart_date}, {self.city}, {self.country},'
                f'{self.Sun_deg},{self.Sun_sign}, {self.Moon_deg},{self.Moon_sign},'
                f' {self.Mercury_deg},{self.Mercury_sign}, {self.Venus_deg},'
                f'{self.Venus_sign}, {self.Mars_deg}, {self.Mars_sign},'
                f'{self.Jupiter_deg},{self.Jupiter_sign},'
                f'{self.Saturn_deg}, {self.Saturn_sign}'
                f'{self.Uranus_deg}, {self.Uranus_sign},'
                f'{self.Neptune_deg}, {self.Neptune_sign},'
                f'{self.Pluto_deg}, {self.Pluto_sign},'
                f'{self.first_house}, {self.asc_deg}, {self.asc_sign},'
                f'{self.second_house}, {self.resource_deg}, {self.resource_sign},'
                f'{self.third_house}, {self.mental_deg}, {self.mental_sign},'
                f'{self.forth_house}, {self.home_deg}, {self.home_sign},'
                f'{self.fifth_house}, {self.game_deg}, {self.game_sign},'
                f'{self. sixth_house}, {self.work_deg}, {self.work_sign},'
                f'{self.seventh_house}, {self.rel_deg}, {self.rel_sign},'
                f'{self.eighth_house}, {self.magic_deg}, {self.magic_sign},'
                f'{self.nineth_house}, {self.esoteric_deg}, {self.esoteric_sign},'
                f'{self.tenth_house}, {self.status_sign}, {self.status_deg},'
                f'{self.eleventh_house}, {self.interests_deg}, {self.interests_sign},'
                f'{self.twelfth_house}, {self.benefits_deg}, {self.benefits_sign}'
                )



class TransitFullChart(models.Model):

    objects = None

    event_name = models.CharField(default='My birthdate')
    event_date = models.DateTimeField(default=timezone.now)
    event_city = models.CharField(default='Ufa')
    event_country = models.CharField(default='Russia')

    transit_name = models.CharField(default='Graduation')
    transit_date = models.DateTimeField(default=timezone.now)
    transit_city = models.CharField(default='Los-Angeles')
    transit_country = models.CharField(default='USA')


    Sun_deg = models.CharField(default='5°05')
    Sun_sign = models.CharField(default='Aquarius')

    Moon_deg = models.CharField(default='14°44')
    Moon_sign = models.CharField(default='Taurus')

    Mercury_deg = models.CharField(default='18°04')
    Mercury_sign = models.CharField(default='Aquarius')

    Venus_deg = models.CharField(default='12°05')
    Venus_sign = models.CharField(default='Aquarius')

    Mars_deg = models.CharField(default='15°21')
    Mars_sign = models.CharField(default='Scorpio')

    Jupiter_deg = models.CharField(default='5°37')
    Jupiter_sign = models.CharField(default='Aquarius')

    Saturn_deg = models.CharField(default='15°18')
    Saturn_sign = models.CharField(default='Scorpio')

    Uranus_deg = models.CharField(default='28°05')
    Uranus_sign = models.CharField(default='Scorpio')

    Neptune_deg = models.CharField(default='11°60')
    Neptune_sign = models.CharField(default='Sagittarius')

    Pluto_deg = models.CharField(default='13°40')
    Pluto_sign = models.CharField(default='Libra')

    first_house = models.CharField(default='Ascendant')
    asc_deg = models.CharField(default='0°')
    asc_sign = models.CharField(default='Aries')

    second_house = models.CharField(default='What you have with & in you')
    resource_deg = models.CharField(default='30°')
    resource_sign = models.CharField(default='Taurus')

    third_house = models.CharField(default='Mentality')
    mental_deg = models.CharField(default='60°')
    mental_sign = models.CharField(default='Gemini')

    forth_house = models.CharField(default='Home')
    home_deg = models.CharField(default='90°')
    home_sign = models.CharField(default='Crab')

    fifth_house = models.CharField(default='Games')
    game_deg = models.CharField(default='120°')
    game_sign = models.CharField(default='Crab')

    sixth_house = models.CharField(default='Work')
    work_deg = models.CharField(default='150°')
    work_sign = models.CharField(default='Virgo')

    seventh_house = models.CharField(default='Relationship')
    rel_deg = models.CharField(default='180°')
    rel_sign = models.CharField(default='Libra')

    eighth_house = models.CharField(default='Magic')
    magic_deg = models.CharField(default='210°')
    magic_sign = models.CharField(default='Scorpio')

    nineth_house = models.CharField(default='Esoteric knowledge')
    esoteric_deg = models.CharField(default='230°')
    esoteric_sign = models.CharField(default='Sagittarius')

    tenth_house = models.CharField(default='Status')
    status_deg = models.CharField(default='260°')
    status_sign = models.CharField(default='Capricorn')

    eleventh_house = models.CharField(default='Interests')
    interests_deg = models.CharField(default='290°')
    interests_sign = models.CharField(default='Aquarius')

    twelfth_house = models.CharField(default='Benefits')
    benefits_deg = models.CharField(default='330°')
    benefits_sign = models.CharField(default='Pisces')


    tr_Sun_deg = models.CharField(default='5°05')
    tr_Sun_sign = models.CharField(default='Aquarius')

    tr_Moon_deg = models.CharField(default='14°44')
    tr_Moon_sign = models.CharField(default='Taurus')

    tr_Mercury_deg = models.CharField(default='18°04')
    tr_Mercury_sign = models.CharField(default='Aquarius')

    tr_Venus_deg = models.CharField(default='12°05')
    tr_Venus_sign = models.CharField(default='Aquarius')

    tr_Mars_deg = models.CharField(default='15°21')
    tr_Mars_sign = models.CharField(default='Scorpio')

    tr_Jupiter_deg = models.CharField(default='5°37')
    tr_Jupiter_sign = models.CharField(default='Aquarius')

    tr_Saturn_deg = models.CharField(default='15°18')
    tr_Saturn_sign = models.CharField(default='Scorpio')

    tr_Uranus_deg = models.CharField(default='28°05')
    tr_Uranus_sign = models.CharField(default='Scorpio')

    tr_Neptune_deg = models.CharField(default='11°60')
    tr_Neptune_sign = models.CharField(default='Sagittarius')

    tr_Pluto_deg = models.CharField(default='13°40')
    tr_Pluto_sign = models.CharField(default='Libra')

    tr_first_house = models.CharField(default='Ascendant')
    tr_asc_deg = models.CharField(default='0°')
    tr_asc_sign = models.CharField(default='Aries')

    tr_second_house = models.CharField(default='What you have with & in you')
    tr_resource_deg = models.CharField(default='30°')
    tr_resource_sign = models.CharField(default='Taurus')

    tr_third_house = models.CharField(default='Mentality')
    tr_mental_deg = models.CharField(default='60°')
    tr_mental_sign = models.CharField(default='Gemini')

    tr_forth_house = models.CharField(default='Home')
    tr_home_deg = models.CharField(default='90°')
    tr_home_sign = models.CharField(default='Crab')

    tr_fifth_house = models.CharField(default='Games')
    tr_game_deg = models.CharField(default='120°')
    tr_game_sign = models.CharField(default='Crab')

    tr_sixth_house = models.CharField(default='Work')
    tr_work_deg = models.CharField(default='150°')
    tr_work_sign = models.CharField(default='Virgo')

    tr_seventh_house = models.CharField(default='Relationship')
    tr_rel_deg = models.CharField(default='180°')
    tr_rel_sign = models.CharField(default='Libra')

    tr_eighth_house = models.CharField(default='Magic')
    tr_magic_deg = models.CharField(default='210°')
    tr_magic_sign = models.CharField(default='Scorpio')

    tr_nineth_house = models.CharField(default='Esoteric knowledge')
    tr_esoteric_deg = models.CharField(default='230°')
    tr_esoteric_sign = models.CharField(default='Sagittarius')

    tr_tenth_house = models.CharField(default='Status')
    tr_status_deg = models.CharField(default='260°')
    tr_status_sign = models.CharField(default='Capricorn')

    tr_eleventh_house = models.CharField(default='Interests')
    tr_interests_deg = models.CharField(default='290°')
    tr_interests_sign = models.CharField(default='Aquarius')

    tr_twelfth_house = models.CharField(default='Benefits')
    tr_benefits_deg = models.CharField(default='330°')
    tr_benefits_sign = models.CharField(default='Pisces')

    tr_chart_image = models.ImageField(upload_to='chart_plots/')
    drawer = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, default=1)


    def __str__(self):
        return (f'{self.event_date}, {self.event_city}, {self.event_country}, {self.event_name},'
                f'{self.Sun_deg},{self.Sun_sign}, {self.Moon_deg},{self.Moon_sign},'
                f' {self.Mercury_deg},{self.Mercury_sign}, {self.Venus_deg},'
                f'{self.Venus_sign}, {self.Mars_deg}, {self.Mars_sign},'
                f'{self.Jupiter_deg},{self.Jupiter_sign},'
                f'{self.Saturn_deg}, {self.Saturn_sign}'
                f'{self.Uranus_deg}, {self.Uranus_sign},'
                f'{self.Neptune_deg}, {self.Neptune_sign},'
                f'{self.Pluto_deg}, {self.Pluto_sign},'
                f'{self.first_house}, {self.asc_deg}, {self.asc_sign},'
                f'{self.second_house}, {self.resource_deg}, {self.resource_sign},'
                f'{self.third_house}, {self.mental_deg}, {self.mental_sign},'
                f'{self.forth_house}, {self.home_deg}, {self.home_sign},'
                f'{self.fifth_house}, {self.game_deg}, {self.game_sign},'
                f'{self.sixth_house}, {self.work_deg}, {self.work_sign},'
                f'{self.seventh_house}, {self.rel_deg}, {self.rel_sign},'
                f'{self.eighth_house}, {self.magic_deg}, {self.magic_sign},'
                f'{self.nineth_house}, {self.esoteric_deg}, {self.esoteric_sign},'
                f'{self.tenth_house}, {self.status_sign}, {self.status_deg},'
                f'{self.eleventh_house}, {self.interests_deg}, {self.interests_sign},'
                f'{self.twelfth_house}, {self.benefits_deg}, {self.benefits_sign},'
                f'{self.transit_date}, {self.transit_city}, {self.transit_country}, {self.transit_name},'
                f'{self.tr_Sun_deg},{self.tr_Sun_sign}, {self.tr_Moon_deg},{self.tr_Moon_sign},'
                f' {self.tr_Mercury_deg},{self.tr_Mercury_sign}, {self.tr_Venus_deg},'
                f'{self.tr_Venus_sign}, {self.tr_Mars_deg}, {self.tr_Mars_sign},'
                f'{self.tr_Jupiter_deg},{self.tr_Jupiter_sign},'
                f'{self.tr_Saturn_deg}, {self.tr_Saturn_sign}'
                f'{self.tr_Uranus_deg}, {self.tr_Uranus_sign},'
                f'{self.tr_Neptune_deg}, {self.tr_Neptune_sign},'
                f'{self.tr_Pluto_deg}, {self.tr_Pluto_sign},'
                f'{self.tr_first_house}, {self.tr_asc_deg}, {self.tr_asc_sign},'
                f'{self.tr_second_house}, {self.tr_resource_deg}, {self.tr_resource_sign},'
                f'{self.tr_third_house}, {self.tr_mental_deg}, {self.tr_mental_sign},'
                f'{self.tr_forth_house}, {self.tr_home_deg}, {self.tr_home_sign},'
                f'{self.tr_fifth_house}, {self.tr_game_deg}, {self.tr_game_sign},'
                f'{self.tr_sixth_house}, {self.tr_work_deg}, {self.tr_work_sign},'
                f'{self.tr_seventh_house}, {self.tr_rel_deg}, {self.tr_rel_sign},'
                f'{self.tr_eighth_house}, {self.tr_magic_deg}, {self.tr_magic_sign},'
                f'{self.tr_nineth_house}, {self.tr_esoteric_deg}, {self.tr_esoteric_sign},'
                f'{self.tr_tenth_house}, {self.tr_status_sign}, {self.tr_status_deg},'
                f'{self.tr_eleventh_house}, {self.tr_interests_deg}, {self.tr_interests_sign},'
                f'{self.tr_twelfth_house}, {self.tr_benefits_deg}, {self.tr_benefits_sign},'
                )





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



# class PlanetData(models.Model):
#
#     planet_name = models.CharField(max_length=20)
#     planet_deg = models.CharField(max_length=16)
#     planet_sign = models.CharField(max_length=16)
#
#
#     def __str__(self):
#         return f'{self.planet_name}, {self.planet_deg}, {self.planet_sign}'


