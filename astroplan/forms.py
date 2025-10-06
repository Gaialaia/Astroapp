from email.policy import default

from Bio.PDB import Select
from django.forms import DateInput, ModelForm
from django.forms.widgets import NumberInput, TextInput
from django_flatpickr.widgets import DatePickerInput, DateTimePickerInput
from django.utils import timezone
from .models import Chart, TransitChart, ZodiacInColors, FullChart, TransitFullChart
import datetime
from colorfield.widgets import ColorWidget
from colorfield.forms import ColorField


from django import forms



class ColorForm(forms.Form):
    color = ColorField(initial="#FF0000")

class TestForm(forms.Form):
    date = forms.DateTimeField(widget=DateTimePickerInput(), label='Enter date')
    city = forms.CharField(label='Enter city')
    country = forms.CharField(label='Enter country')

    class Media:
        css = {
            'all': ['/static/styles/form_style.css']
        }


class FullChartForm(forms.ModelForm):
    class Meta:
        model = FullChart
        fields = ['chart_name','chart_date', 'city', 'country']
        labels = {'chart_name':'Enter event name',
                'chart_date': 'Enter date',
                'city': 'Enter city',
                'country': 'Enter country'
                  }
        widgets = {
            'chart_date': DateTimePickerInput()}

        class Media:
            css = {
                'all': ['/static/styles/form_style.css']
            }


class ChartForm(forms.ModelForm):
    class Meta:
        model = Chart
        fields = ['chart_date', 'city', 'country']
        labels = {'chart_date': 'Enter date',
                  'city': 'Enter city',
                  'country': 'Enter country'
                  }
        widgets = {
            'chart_date': DateTimePickerInput()}

        class Media:
            css = {
                'all': ['/static/styles/form_style.css']
            }

class TransitForm(forms.Form):

    event_date = forms.DateTimeField(widget=DateTimePickerInput(), label='Enter event date')
    event_city = forms.CharField(label='Enter event city')
    event_country = forms.CharField(label='Enter event country')

    transit_date = forms.DateTimeField(widget=DateTimePickerInput(), label='Enter transit date')
    transit_city = forms.CharField(label='Enter transit city')
    transit_country = forms.CharField(label='Enter transit country')

    class Media:
        css = {
            'all': ['/static/styles/form_style.css']
        }

class TransitFullChartForm(forms.ModelForm):

    class Meta:
        model = TransitFullChart

        fields = ['event_name', 'event_date',
                  'event_city', 'event_country',
                  'transit_name', 'transit_date',
                  'transit_city', 'transit_country',
                  ]

        widgets = {'event_chart_date': DateTimePickerInput,
                   'transit_chart_date':DateTimePickerInput}


        labels = {'event_chart_date': 'Enter an event date',
                  'event_chart_city': 'Enter city',
                  'event_chart_country': 'Enter country',
                  'transit_chart_date': 'Enter transit date',
                  'transit_chart_city':  'Enter city',
                  'transit_chart_country': 'Enter country',
                  }

        class Media:
            css = {
                'all': ['/static/styles/form_style.css']
            }


class ZodiacInColorForm(forms.ModelForm):
    
    class Meta:
        model = ZodiacInColors
        fields = '__all__'
        
        widgets = {'chart_date': DateTimePickerInput()}
        
        labels = {'track_aries_axis_fc': 'Aries axis face color',
                  'track_aries_axis_ec' :'Aries axis edge color',
                  'track_aries_axis_tc' : 'Aries text color',

                  'track_leo_axis_fc': 'Leo axis face color',
                  'track_leo_axis_ec': 'Leo axis edge color',
                  'track_leo_axis_tc': 'Leo text color',

                  'track_sag_axis_fc' : 'Sagittarius axis face color',
                  'track_sag_axis_ec': 'Sagittarius axis edge color',
                  'track_sag_axis_tc': 'Sagittarius text color',
                  
                  'track_aqua_axis_fc': 'Aquarius axis face color',
                  'track_aqua_axis_ec': 'Aquarius axis edge color',
                  'track_aqua_axis_tc': 'Aquarius text color',
                  
                  'track_gemini_axis_fc': 'Gemini axis face color',
                  'track_gemini_axis_ec':'Gemini axis edge color',
                  'track_gemini_axis_tc': 'Gemini text color',

                  'track_libra_axis_fc':'Libra axis face color',
                  'track_libra_axis_ec': 'Libra axis edge color',
                  'track_libra_axis_tc':'Libra text color',

                  'track_scorpio_axis_fc': 'Scorpio axis face color',
                  'track_scorpio_axis_ec': 'Scorpio axis edge color',
                  'track_scorpio_axis_tc': 'Scorpio text color',
                  
                  'track_cancer_axis_fc': 'Cancer axis face color',
                  'track_cancer_axis_ec': 'Cancer axis edge color',
                  'track_cancer_axis_tc': 'Cancer text color',

                  'track_pisces_axis_fc' : 'Pisces axis face color',
                  'track_pisces_axis_ec': 'Pisces axis edge color',
                  'track_pisces_axis_tc': 'Pisces text color',                  # 
                  
                  'track_taurus_axis_fc': 'Taurus axis face color',
                  'track_taurus_axis_ec': 'Taurus axis edge color',
                  'track_taurus_axis_tc': 'Taurus text color',
                  
                  'track_virgo_axis_fc' : 'Virgo axis face color',
                  'track_virgo_axis_ec': 'Virgo axis edge color',
                  'track_virgo_axis_tc': 'Virgo text color',
                  
                  'track_capricorn_axis_fc': 'Capricorn axis face color',
                  'track_capricorn_axis_ec':'Capricorn axis edge color',
                  'track_capricorn_axis_tc':'Capricorn text color',
                  
                  'degrees_track_ec' : 'Degrees track face color',
                  'degrees_ticks_color' : 'Degrees tick color',
                  
                   
                  'sun_symbol_c': 'Sun symbol color',
                  'sun_symbol_s' : 'Sun symbol size',
                  'sun_marker_c': 'Sun marker color',

                  'moon_symbol_c' : 'Moon symbol color',
                  'moon_symbol_s' : 'Moon symbol size',
                  'moon_marker_c' : 'Moon marker color',

                  'mercury_symbol_c': 'Mercury symbol color',
                  'mercury_symbol_s' : 'Mercury symbol size',
                  'mercury_marker_c' :'Mercury symbol color',

                  'venus_symbol_c': 'Venus symbol color',
                  'venus_symbol_s' :'Venus symbol size',
                  'marker_cVenus' : 'marker color',

                  'mars_symbol_c': 'Mars symbol color',
                  'mars_symbol_s' : 'Mars symbol size',
                  'mars_marker_c': 'Mars marker color',


                  'jupiter_symbol_c':'Jupiter symbol color',
                  'jup_symbol_s' :'Jupiter symbol size',
                  'jup_marker_c' : 'Jupiter marker color',

                  'saturn_symbol_c': 'Saturn symbol color',
                  'saturn_symbol_s' :'Saturn symbol size',
                  'saturn_marker_c': 'Saturn marker color',

                  'uranus_symbol_c': 'Uranus symbol color',
                  'uranus_symbol_s' :'Uranus symbol size',
                  'uranus_marker_c':'Uranus marker color',

                  'neptune_symbol_c':'Neptune symbol color',
                  'neptune_symbol_s' : 'Neptune symbol size',
                  'neptune_marker_c':'Neptune marker color',


                  'pluto_symbol_c' : 'Pluto symbol color',
                  'pluto_symbol_s' : 'Pluto symbol size',
                  'pluto_marker_c': 'Pluto marker color',

                  }

    class Media:
            css = {
            ' all': ['/static/styles/form_style.css']}
        
                

class ColorfulZodiacForm(forms.Form):

    COLORS_CHOICES = (
        ("DarkRed", "DarkRed"),
        ("Red", "Red"),
        ("Salmon", "Salmon"),
        ("MediumVioletRed","MediumVioletRed"),
        ("HotPink", "HotPink"),
        ("DeepPink", "DeepPink"),
        ("OrangeRed", "OrangeRed"),
        ("Gold","Gold"),
        ("Yellow", "Yellow"),
        ("Indigo", "Indigo"),
        ("DarkOrchid", "DarkOrchid"),
        ("SlateBlue","SlateBlue"),
       ("Teal","Teal"),
       ("Olive","Olive"),
       ("YellowGreen","YellowGreen"),
       ("Chartreuse","Chartreuse"),
       ("ForestGreen","ForestGreen"),
       ("MidnightBlue","MidnightBlue"),
       ("DodgerBlue","DodgerBlue"),
       ("DarkTurquoise","DarkTurquoise"),
       ("SaddleBrown","SaddleBrown"),
       ("SaddleBrown","SandyBrown"),
       ("Wheat","Wheat"),
       ("WhiteSmoke","WhiteSmoke"),
       ("AliceBlue","AliceBlue"),
       ("LavenderBlush","LavenderBlush"),
       ("Gray","Gray"),
       ("DarkSlateGray","DarkSlateGray"),
       ("DimGray","DimGray"),
       ("BurlyWood","BurlyWood"),
       ("",""),
       ("",""),
       ("",""),
       ("",""),
    )



    cz_chart_date = (forms.DateTimeField
                     (widget=DateTimePickerInput(attrs={'class':'form-control',
                    'id':'chart-date'}), label='Enter chart date'))
    cz_chart_city = forms.CharField(label='Enter city', widget=TextInput(attrs={'class':'form-control','placeholder':'city',
                                                                                'id':'chart-city'}))
    cz_chart_country = forms.CharField(label='Enter country',  widget=TextInput(attrs={'class':'form-control',
                                                                                       'id':'chart-country'}))


    # track_aries_axis_fc = forms.ChoiceField(choices=COLORS_CHOICES,
    #                                         widget=forms.Select(attrs={'class':'form-control',
    #                                                                    'id':'aries-fc', 'type':'color'}))
    #
    #
    # track_aries_axis_ec = forms.ChoiceField(choices=COLORS_CHOICES,
    #                                         widget=forms.Select(attrs={'class':'form-control',
    #                                                                    'id':'aries-ec'}))
    # track_aries_axis_tc = forms.ChoiceField(choices=COLORS_CHOICES,
    #                                         widget=forms.Select(attrs={'class': 'form-control',
    #                                                                    'id': 'aries-tc'}))



    # track_aries_axis_fc = forms.TextInput(attrs={'type': 'color', 'class': 'form-control', 'id': 'aries-fc'})
    track_aries_axis_fc = ColorField(widget=ColorWidget(attrs={'class': 'form-control', 'id': 'aries-fc'}), label='fc')
    track_aries_axis_ec = ColorField(widget=ColorWidget(attrs={'class': 'form-control', 'id': 'aries-ec'}), label='ec')
    track_aries_axis_tc = ColorField(widget=ColorWidget(attrs={'class': 'form-control', 'id': 'aries-tc'}), label='tc')
    #
    # track_aries_axis_fc = forms.TextInput(attrs={'type': 'color'})

    #
    # track_leo_axis_fc = forms.ChoiceField(choices=COLORS_CHOICES,
    #                                       widget=forms.Select(attrs={'class': 'form-control',
    #                                                                  'id': 'leo-tc'}))
    # track_leo_axis_ec = forms.ChoiceField(choices=COLORS_CHOICES,
    #                                       widget=forms.Select(attrs={'class': 'form-control',
    #                                                                  'id': 'leo-tc'}))
    # track_leo_axis_tc = forms.ChoiceField(choices=COLORS_CHOICES,
    #                                       widget=forms.Select(attrs={'class': 'form-control',
    #                                                                  'id': 'leo-tc'}))

    track_leo_axis_fc = ColorField(widget=ColorWidget(attrs={'class': 'form-control', 'id': 'leo-fc'}))
    track_leo_axis_ec = ColorField(widget=ColorWidget(attrs={'class': 'form-control', 'id': 'leo-ec'}))
    track_leo_axis_tc = ColorField(widget=ColorWidget(attrs={'class': 'form-control', 'id': 'leo-tc'}))

    # track_sag_axis_fc = forms.ChoiceField(choices=COLORS_CHOICES,
    #                                       widget=forms.Select(attrs={'class':'form-control', 'id':'sag-fc'}))
    # track_sag_axis_ec = forms.ChoiceField(choices=COLORS_CHOICES,
    #                                       widget=forms.Select(attrs={'class': 'form-control', 'id': 'sag-ec'}))
    # track_sag_axis_tc = forms.ChoiceField(choices=COLORS_CHOICES,
    #                                       widget=forms.Select(attrs={'class': 'form-control', 'id': 'sag-tc'}))

    track_sag_axis_fc = ColorField(initial='#F87230',
                                   widget=ColorWidget(attrs={'class': 'form-control', 'id': 'sag-fc'}))
    track_sag_axis_ec = ColorField(widget=ColorWidget(attrs={'class': 'form-control', 'id': 'sag-ec'}))
    track_sag_axis_tc = ColorField(widget=ColorWidget(attrs={'class': 'form-control', 'id': 'sag-tc'}))

    # track_aqua_axis_fc = forms.ChoiceField(choices=COLORS_CHOICES,
    #                                        widget=forms.Select(attrs={'class': 'form-control', 'id': 'aqua-fc'}))
    # track_aqua_axis_ec = forms.ChoiceField(choices=COLORS_CHOICES,
    #                                        widget=forms.Select(attrs={'class': 'form-control', 'id': 'aqua-ec'}))
    # track_aqua_axis_tc = forms.ChoiceField(choices=COLORS_CHOICES,
    #                                        widget=forms.Select(attrs={'class': 'form-control', 'id': 'aqua-tc'}))

    track_aqua_axis_fc = ColorField(initial='#F87230',
                                   widget=ColorWidget(attrs={'class': 'form-control', 'id': 'aqua-fc'}))
    track_aqua_axis_ec = ColorField(widget=ColorWidget(attrs={'class': 'form-control', 'id': 'aqua-ec'}))
    track_aqua_axis_tc = ColorField(widget=ColorWidget(attrs={'class': 'form-control', 'id': 'aqua-tc'}))



    # track_gemini_axis_fc = forms.ChoiceField(choices=COLORS_CHOICES,
    #                                          widget=forms.Select(attrs={'class': 'form-control', 'id': 'gemini-fc'}))
    # track_gemini_axis_ec = forms.ChoiceField(choices=COLORS_CHOICES,
    #                                          widget=forms.Select(attrs={'class': 'form-control', 'id': 'gemini-ec'}))
    # track_gemini_axis_tc = forms.ChoiceField(choices=COLORS_CHOICES,
    #                                          widget=forms.Select(attrs={'class': 'form-control', 'id': 'gemini-tc'}))

    track_gemini_axis_fc = ColorField(initial='#F87230',
                                   widget=ColorWidget(attrs={'class': 'form-control', 'id': 'gemini-fc'}))
    track_gemini_axis_ec = ColorField(widget=ColorWidget(attrs={'class': 'form-control', 'id': 'gemini-ec'}))
    track_gemini_axis_tc = ColorField(widget=ColorWidget(attrs={'class': 'form-control', 'id': 'gemini-tc'}))

    # track_libra_axis_fc = forms.ChoiceField(choices=COLORS_CHOICES,
    #                                         widget=forms.Select(attrs={'class': 'form-control', 'id': 'libra-fc'}))
    # track_libra_axis_ec = forms.ChoiceField(choices=COLORS_CHOICES,
    #                                         widget=forms.Select(attrs={'class': 'form-control', 'id': 'libra-ec'}))
    # track_libra_axis_tc = forms.ChoiceField(choices=COLORS_CHOICES,
    #                                         widget=forms.Select(attrs={'class': 'form-control', 'id': 'libra-tc'}))

    track_libra_axis_fc = ColorField(initial='#F87230',
                                   widget=ColorWidget(attrs={'class': 'form-control', 'id': 'libra-fc'}))
    track_libra_axis_ec = ColorField(widget=ColorWidget(attrs={'class': 'form-control', 'id': 'libra-ec'}))
    track_libra_axis_tc = ColorField(widget=ColorWidget(attrs={'class': 'form-control', 'id': 'libra-tc'}))

    # track_scorpio_axis_fc = forms.ChoiceField(choices=COLORS_CHOICES,
    #                                           widget=forms.Select(attrs={'class': 'form-control', 'id': 'scorpio-fc'}))
    # track_scorpio_axis_ec = forms.ChoiceField(choices=COLORS_CHOICES,
    #                                           widget=forms.Select(attrs={'class': 'form-control', 'id': 'scorpio-ec'}))
    # track_scorpio_axis_tc = forms.ChoiceField(choices=COLORS_CHOICES,
    #                                           widget=forms.Select(attrs={'class': 'form-control', 'id': 'scorpio-tc'}))
    track_scorpio_axis_fc = ColorField(initial='#F87230',
                                     widget=ColorWidget(attrs={'class': 'form-control', 'id': 'scorpio-fc'}))
    track_scorpio_axis_ec = ColorField(widget=ColorWidget(attrs={'class': 'form-control', 'id': 'scorpio-ec'}))
    track_scorpio_axis_tc = ColorField(widget=ColorWidget(attrs={'class': 'form-control', 'id': 'scorpio-tc'}))


    # track_cancer_axis_fc = forms.ChoiceField(choices=COLORS_CHOICES,
    #                                          widget=forms.Select(attrs={'class': 'form-control', 'id': 'cancer-fc'}))
    # track_cancer_axis_ec = forms.ChoiceField(choices=COLORS_CHOICES,
    #                                          widget=forms.Select(attrs={'class': 'form-control', 'id': 'cancer-ec'}))
    # track_cancer_axis_tc = forms.ChoiceField(choices=COLORS_CHOICES,
    #                                          widget=forms.Select(attrs={'class': 'form-control', 'id': 'cancer-tc'}))

    track_cancer_axis_fc = ColorField(initial='#F87230',
                                     widget=ColorWidget(attrs={'class': 'form-control', 'id': 'cancer-fc'}))
    track_cancer_axis_ec = ColorField(widget=ColorWidget(attrs={'class': 'form-control', 'id': 'cancer-ec'}))
    track_cancer_axis_tc = ColorField(widget=ColorWidget(attrs={'class': 'form-control', 'id': 'cancer-tc'}))

    # track_pisces_axis_fc = forms.ChoiceField(choices=COLORS_CHOICES,
    #                                          widget=forms.Select(attrs={'class': 'form-control', 'id': 'pisces-fc'}))
    # track_pisces_axis_ec = forms.ChoiceField(choices=COLORS_CHOICES,
    #                                          widget=forms.Select(attrs={'class': 'form-control', 'id': 'pisces-ec'}))
    # track_pisces_axis_tc = forms.ChoiceField(choices=COLORS_CHOICES,
    #                                          widget=forms.Select(attrs={'class': 'form-control', 'id': 'pisces-tc'}))

    track_pisces_axis_fc = ColorField(initial='#F87230',
                                     widget=ColorWidget(attrs={'class': 'form-control', 'id': 'pisces-fc'}))
    track_pisces_axis_ec = ColorField(widget=ColorWidget(attrs={'class': 'form-control', 'id': 'pisces-ec'}))
    track_pisces_axis_tc = ColorField(widget=ColorWidget(attrs={'class': 'form-control', 'id': 'pisces-tc'}))

    # track_taurus_axis_fc = forms.ChoiceField(choices=COLORS_CHOICES,
    #                                          widget=forms.Select(attrs={'class': 'form-control', 'id': 'taurus-fc'}))
    # track_taurus_axis_ec = forms.ChoiceField(choices=COLORS_CHOICES,
    #                                          widget=forms.Select(attrs={'class': 'form-control', 'id': 'taurus-ec'}))
    # track_taurus_axis_tc = forms.ChoiceField(choices=COLORS_CHOICES,
    #                                          widget=forms.Select(attrs={'class': 'form-control', 'id': 'taurus-tc'}))

    track_taurus_axis_fc = ColorField(initial='#F87230',
                                     widget=ColorWidget(attrs={'class': 'form-control', 'id': 'taurus-fc'}))
    track_taurus_axis_ec = ColorField(widget=ColorWidget(attrs={'class': 'form-control', 'id': 'taurus-ec'}))
    track_taurus_axis_tc = ColorField(widget=ColorWidget(attrs={'class': 'form-control', 'id': 'taurus-tc'}))

    # track_virgo_axis_fc = forms.ChoiceField(choices=COLORS_CHOICES,
    #                                         widget=forms.Select(attrs={'class': 'form-control', 'id': 'virgo-fc'}))
    # track_virgo_axis_ec = forms.ChoiceField(choices=COLORS_CHOICES,
    #                                         widget=forms.Select(attrs={'class': 'form-control', 'id': 'virgo-ec'}))
    # track_virgo_axis_tc = forms.ChoiceField(choices=COLORS_CHOICES,
    #                                         widget=forms.Select(attrs={'class': 'form-control', 'id': 'virgo-tc'}))

    track_capricorn_axis_fc = ColorField(initial='#F87230',
                                     widget=ColorWidget(attrs={'class': 'form-control', 'id': 'capricorn-fc'}))
    track_capricorn_axis_ec = ColorField(widget=ColorWidget(attrs={'class': 'form-control', 'id': 'capricorn-ec'}))
    track_capricorn_axis_tc = ColorField(widget=ColorWidget(attrs={'class': 'form-control', 'id': 'capricorn-tc'}))

    # track_capricorn_axis_fc = forms.ChoiceField(choices=COLORS_CHOICES,
    #                                             widget=forms.Select(attrs={'class': 'form-control', 'id': 'capricorn-fc'}))
    # track_capricorn_axis_ec = forms.ChoiceField(choices=COLORS_CHOICES,
    #                                             widget=forms.Select(attrs={'class': 'form-control', 'id': 'capricorn-ec'}))
    # track_capricorn_axis_tc = forms.ChoiceField(choices=COLORS_CHOICES,
    #                                             widget=forms.Select(attrs={'class': 'form-control', 'id': 'capricorn-tc'}))

    track_virgo_axis_fc = ColorField(initial='#F87230',
                                     widget=ColorWidget(attrs={'class': 'form-control', 'id': 'virgo-fc'}))
    track_virgo_axis_ec = ColorField(widget=ColorWidget(attrs={'class': 'form-control', 'id': 'virgo-ec'}))
    track_virgo_axis_tc = ColorField(widget=ColorWidget(attrs={'class': 'form-control', 'id': 'virgo-tc'}))

    # degrees_track_ec = forms.ChoiceField(choices=COLORS_CHOICES,
    #                                      widget=forms.Select(attrs={'class': 'form-control', 'id': 'deg-ec'}))
    # degrees_ticks_color = forms.ChoiceField(choices=COLORS_CHOICES,
    #                                         widget=forms.Select(attrs={'class': 'form-control', 'id': 'tick-cl'}))


    degrees_track_ec = ColorField(widget=ColorWidget(attrs={'class': 'form-control', 'id': 'deg-ec'}), label='degrees track color')

    degrees_ticks_color = ColorField(widget=ColorWidget(attrs={'class': 'form-control', 'id': 'tick-cl'}), label='degrees ticks color')


    # sun_symbol_c = forms.ChoiceField(choices=COLORS_CHOICES,
    #                                  widget=forms.Select(attrs={'class': 'form-control', 'id':'sun-sm'}))
    # sun_symbol_s = forms.IntegerField()
    # sun_marker_c = forms.ChoiceField(choices=COLORS_CHOICES,
    #                                  widget=forms.Select(attrs={'class': 'form-control', 'id':'sun-mk'}))

    sun_symbol_c = ColorField(widget=ColorWidget(attrs={'class': 'form-control', 'id': 'sun-sm'}))
    sun_marker_c = ColorField(widget=ColorWidget(attrs={'class': 'form-control', 'id': 'sun-mk'}))
    sun_symbol_s = forms.IntegerField()

    # moon_symbol_c = forms.ChoiceField(choices=COLORS_CHOICES,
    #                                   widget=forms.Select(attrs={'class': 'form-control', 'id': 'moon-sm'}))
    # moon_symbol_s = forms.IntegerField()
    # moon_marker_c = forms.ChoiceField(choices=COLORS_CHOICES,
    #                                   widget=forms.Select(attrs={'class': 'form-control', 'id': 'moon-mk'}))

    moon_symbol_c = ColorField(widget=ColorWidget(attrs={'class': 'form-control', 'id': 'moon-sm'}))
    moon_marker_c = ColorField(widget=ColorWidget(attrs={'class': 'form-control', 'id': 'moon-mk'}))
    moon_symbol_s = forms.IntegerField()

    # mercury_symbol_c = forms.ChoiceField(choices=COLORS_CHOICES,
    #                                      widget=forms.Select(attrs={'class': 'form-control', 'id': 'mercury-sm'}))
    # mercury_symbol_s = forms.IntegerField()
    # mercury_marker_c = forms.ChoiceField(choices=COLORS_CHOICES,
    #                                      widget=forms.Select(attrs={'class': 'form-control', 'id': 'mercury-mk'}))

    mercury_symbol_c = ColorField(widget=ColorWidget(attrs={'class': 'form-control', 'id': 'mercury-sm'}))
    mercury_marker_c = ColorField(widget=ColorWidget(attrs={'class': 'form-control', 'id': 'mercury-mk'}))
    mercury_symbol_s = forms.IntegerField()


    # venus_symbol_c = forms.ChoiceField(choices=COLORS_CHOICES,
    #                                    widget=forms.Select(attrs={'class': 'form-control', 'id': 'venus-sm'}))
    # venus_symbol_s = forms.IntegerField()
    # venus_marker_c = forms.ChoiceField(choices=COLORS_CHOICES,
    #                                    widget=forms.Select(attrs={'class': 'form-control', 'id': 'venus-mk'}))

    venus_symbol_c = ColorField(widget=ColorWidget(attrs={'class': 'form-control', 'id': 'venus-sm'}))
    venus_marker_c = ColorField(widget=ColorWidget(attrs={'class': 'form-control', 'id': 'venus-mk'}))
    venus_symbol_s = forms.IntegerField()

    # mars_symbol_c = forms.ChoiceField(choices=COLORS_CHOICES,
    #                                   widget=forms.Select(attrs={'class': 'form-control', 'id': 'mars-mk'}))
    # mars_symbol_s = forms.IntegerField(widget=NumberInput)
    # mars_marker_c = forms.ChoiceField(choices=COLORS_CHOICES,
    #                                   widget=forms.Select(attrs={'class': 'form-control', 'id': 'mars-mk'}))

    mars_symbol_c = ColorField(widget=ColorWidget(attrs={'class': 'form-control', 'id': 'mars-sm'}), label='msc')
    mars_marker_c = ColorField(widget=ColorWidget(attrs={'class': 'form-control', 'id': 'mars-mk'}))
    mars_symbol_s = forms.IntegerField()

    # jupiter_symbol_c = forms.ChoiceField(choices=COLORS_CHOICES,
    #                                      widget=forms.Select(attrs={'class': 'form-control', 'id': 'jupiter-sm'}))
    # jup_symbol_s = forms.IntegerField()
    # jup_marker_c = forms.ChoiceField(choices=COLORS_CHOICES,
    #                                  widget=forms.Select(attrs={'class': 'form-control', 'id':'jup-mk'}))

    jupiter_symbol_c = ColorField(widget=ColorWidget(attrs={'class': 'form-control', 'id': 'jup-sm'}))
    jup_marker_c = ColorField(widget=ColorWidget(attrs={'class': 'form-control', 'id': 'jup-mk'}))
    jup_symbol_s = forms.IntegerField()

    # saturn_symbol_c = forms.ChoiceField(choices=COLORS_CHOICES,
    #                                     widget=forms.Select(attrs={'class': 'form-control', 'id': 'saturn-sm'}))
    # saturn_symbol_s = forms.IntegerField()
    # saturn_marker_c = forms.ChoiceField(choices=COLORS_CHOICES,
    #                                     widget=forms.Select(attrs={'class': 'form-control', 'id': 'saturn-mk'}))

    saturn_symbol_c = ColorField(widget=ColorWidget(attrs={'class': 'form-control', 'id': 'saturn-sm'}))
    saturn_marker_c = ColorField(widget=ColorWidget(attrs={'class': 'form-control', 'id': 'saturn-mk'}))
    saturn_symbol_s = forms.IntegerField()

    # uranus_symbol_c = forms.ChoiceField(choices=COLORS_CHOICES,
    #                                     widget=forms.Select(attrs={'class': 'form-control', 'id':'uranus-sm'}))
    # uranus_symbol_s = forms.IntegerField()
    # uranus_marker_c = forms.ChoiceField(choices=COLORS_CHOICES,
    #                                     widget=forms.Select(attrs={'class': 'form-control', 'id': 'uranus-mk'}))

    uranus_symbol_c = ColorField(widget=ColorWidget(attrs={'class': 'form-control', 'id': 'uranus-sm'}))
    uranus_marker_c = ColorField(widget=ColorWidget(attrs={'class': 'form-control', 'id': 'uranus-mk'}))
    uranus_symbol_s = forms.IntegerField()

    # neptune_symbol_c = forms.ChoiceField(choices=COLORS_CHOICES,
    #                                      widget=forms.Select(attrs={'class': 'form-control', 'id': 'neptune-sm'}))
    # neptune_symbol_s = forms.IntegerField()
    # neptune_marker_c = forms.ChoiceField(choices=COLORS_CHOICES,
    #                                      widget=forms.Select(attrs={'class': 'form-control', 'id': 'neptune-mk'}))

    neptune_symbol_c = ColorField(widget=ColorWidget(attrs={'class': 'form-control', 'id': 'neptune-sm'}))
    neptune_marker_c = ColorField(widget=ColorWidget(attrs={'class': 'form-control', 'id': 'neptune-mk'}))
    neptune_symbol_s = forms.IntegerField()

    # pluto_symbol_c = forms.ChoiceField(choices=COLORS_CHOICES,
    #                                    widget=forms.Select(attrs={'class': 'form-control', 'id': 'pluto-sm'}))
    # pluto_symbol_s = forms.IntegerField()
    # pluto_marker_c = forms.ChoiceField(choices=COLORS_CHOICES,
    #                                    widget=forms.Select(attrs={'class': 'form-control', 'id': 'pluto-mk'}))

    pluto_symbol_c = ColorField(widget=ColorWidget(attrs={'class': 'form-control', 'id': 'pluto-sm'}))
    pluto_marker_c = ColorField(widget=ColorWidget(attrs={'class': 'form-control', 'id': 'pluto-mk'}))
    pluto_symbol_s = forms.IntegerField()



    # class Media:
    #     css = {
    #         'all': ['/static/styles/form_style.css']
    #     }


   
   
    
   
  








