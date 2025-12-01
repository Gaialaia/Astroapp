from django import forms
from django.forms.widgets import TextInput, Select
from django_flatpickr.widgets import DatePickerInput, DateTimePickerInput
from django.utils import timezone

from .models import Chart, TransitChart, ZodiacInColors, FullChart, TransitFullChart,OneColorZodiacRingMF

from colorfield.widgets import ColorWidget
from colorfield.forms import ColorField


import swisseph as swe

SIDEREAL = swe.FLG_SIDEREAL
TROPICAL = swe.FLG_TROPICAL
HELIOCENTRIC = swe.FLG_HELCTR


MODE_CHOICES = {
        SIDEREAL: 'Sidereal',
        TROPICAL: 'Tropical',
        HELIOCENTRIC: 'Heliocentric',
        }

PlACIDUS = 'P'
REGIONMONTANUS = 'R'
EQUAL = 'E'

HOUSE_SYSTEM_CHOICES = \
    {
        PlACIDUS : 'Placidus',
        REGIONMONTANUS : 'Regiomontanus',
        EQUAL :  'Equal',
        'Without houses': 'Without houses',
    }



class ChartForm(forms.ModelForm):
    class Meta:
        model = Chart
        fields = '__all__'
        labels = {'chart_date': 'Enter date',
                  'city': 'Enter city',
                  'country': 'Enter country',
                  'chart_mode': 'Chose chart mode: ',
                  'house_system': 'Chose house system:'

                  }
        widgets = {
            'chart_date': DateTimePickerInput()}

        class Media:
            css = {
                'all': ['/static/styles/form_style.css']
            }

class ShowChart(forms.Form):

    chart_date = forms.DateTimeField(widget=DateTimePickerInput(), label='Enter date', initial=timezone.now())
    city = forms.CharField(label='Enter city', initial='Ufa')
    country = forms.CharField(label='Enter country', initial='Russia')

    mode = forms.ChoiceField(label = 'Chose chart mode', choices=MODE_CHOICES, initial='Sidereal', widget=forms.Select)
    house_system = forms.ChoiceField(label='Chose house system',choices=HOUSE_SYSTEM_CHOICES, initial='Regiomontanus')

    class Media:
        css = {
            'all': ['/static/styles/form_style.css']
        }


class TransitForm(forms.Form):

    event_date = forms.DateTimeField(widget=DateTimePickerInput(), label='Enter event date', initial=timezone.now())
    event_city = forms.CharField(label='Enter event city', initial='Ufa')
    event_country = forms.CharField(label='Enter event country', initial='Russia')

    ev_mode = forms.ChoiceField(label='Chose event chart mode', choices=MODE_CHOICES, initial='Sidereal', widget=forms.Select)
    ev_house_system = forms.ChoiceField(label='Chose event house system',
                                        choices=HOUSE_SYSTEM_CHOICES, initial='Regiomontanus',
                                        widget=forms.Select)

    transit_date = forms.DateTimeField(widget=DateTimePickerInput(), label='Enter transit date')
    transit_city = forms.CharField(label='Enter transit city', initial='Ufa')
    transit_country = forms.CharField(label='Enter transit country', initial='Russia')

    tr_mode = forms.ChoiceField(label='Chose transit chart mode', choices=MODE_CHOICES, initial='Sidereal',
                                widget=forms.Select)
    tr_house_system = forms.ChoiceField(label='Chose transit house system', choices=HOUSE_SYSTEM_CHOICES,
                                        initial='Regiomontanus', widget=forms.Select)

    class Media:
        css = {
            'all': ['/static/styles/form_style.css']
        }


class FullChartForm(forms.ModelForm):
    class Meta:
        model = FullChart
        fields = ['chart_name','chart_date', 'city', 'country', 'chart_mode', 'house_system']
        labels = {'chart_name':'Enter event name',
                'chart_date': 'Enter date',
                'city': 'Enter city',
                'country': 'Enter country',
                'chart_mode': 'Chose chart mode: ',
                'house_system': 'Chose house system:'
                  }
        widgets = {
            'chart_date': DateTimePickerInput(),
            'chart_mode': Select(),
            'house_system': Select(),

        }

        class Media:
            css = {
                'all': ['/static/styles/form_style.css']
            }







class TransitFullChartForm(forms.ModelForm):

    class Meta:
        model = TransitFullChart

        fields = ['event_name', 'event_date',
                  'event_city', 'event_country',
                  'ev_chart_mode', 'ev_house_system',
                  'transit_name', 'transit_date',
                  'transit_city', 'transit_country',
                  'tr_chart_mode', 'tr_house_system',
                  ]

        widgets = {'event_date': DateTimePickerInput(),
                   'transit_date':DateTimePickerInput()}


        labels = {'event_date': 'Enter an event date',
                  'event_city': 'Enter city',
                  'event_country': 'Enter country',
                  'ev_chart_mode': 'Enter event mode: ',
                  'ev_house_system': 'Enter house system',

                  'transit_date': 'Enter transit date',
                  'transit_city':  'Enter city',
                  'transit_country': 'Enter country',
                  'tr_chart_mode': 'Enter event mode: ',
                  'tr_house_system': 'Enter house system',
                  }

        class Media:
            css = {
                'all': ['/static/styles/form_style.css']
            }


class OneColorZodiacRing(forms.Form):
    # auto_id = True
    oc_chart_date = (forms.DateTimeField
                     (widget=DateTimePickerInput(attrs={'class': 'form-control',
                                                        'id': 'chart-date'}), label='Enter chart date',
                      initial=timezone.now()))
    oc_chart_city = forms.CharField(label='Enter city', initial='Ufa',
                                    widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'city',
                                                            'id': 'chart-city'}))
    oc_chart_country = forms.CharField(label='Enter country', widget=TextInput(attrs={'class': 'form-control',
                                                                                      'id': 'chart-country'}),
                                       initial='Russia')

    one_clr_zr_chart_mode = forms.ChoiceField(label='Chose event chart mode', choices=MODE_CHOICES, initial='Sidereal', widget=forms.Select)
    one_clr_zr_chart_hs = forms.ChoiceField(label='Chose event house system', choices=HOUSE_SYSTEM_CHOICES, initial='Regiomontanus')

    face_color = ColorField(widget=ColorWidget(attrs={'class': 'form-control', 'id': 'face-color'}),
                            label='Enter face color', initial='#300c63')
    edge_color = ColorField(widget=ColorWidget(attrs={'class': 'form-control', 'id': 'edge-color'}),
                            label='Enter edge color', initial='#3dffc8')
    text_color = ColorField(widget=ColorWidget(attrs={'class': 'form-control', 'id': 'text-color'}),
                            label='Enter zodiac symbol color', initial='#3dffc8')
    tick_color = ColorField(widget=ColorWidget(attrs={'class': 'form-control', 'id': 'tick-color'}),
                            label='Enter tick color', initial='#63ffd3')
    deg_color = ColorField(widget=ColorWidget(attrs={'class': 'form-control', 'id': 'deg-color'}),
                           label='Enter degree tick color', initial='#63ffd3')
    marker_color = ColorField(widget=ColorWidget(attrs={'class': 'form-control', 'id': 'marker-color'}),
                              label='Enter planet symbol marker color', initial='#ffc83d')
    symbol_color = ColorField(widget=ColorWidget(attrs={'class': 'form-control', 'id': 'symbol-color'}),
                              label='Enter planet symbol color', initial='#ff3d74')

    house_ax_color = ColorField(widget=ColorWidget(attrs={'class': 'form-control', 'id': 'ha-color'}),
                                label='Enter house ax color', initial='#ffc83d')
    house_number_color = ColorField(widget=ColorWidget(attrs={'class': 'form-control', 'id': 'hnum-color'}),
                                    label='Enter house number color', initial='#ffc83d')
    house_track_color = ColorField(widget=ColorWidget(attrs={'class': 'form-control', 'id': 'htr-color'}),
                                   label='Enter house track color', initial='#ffc83d')

    marker_size = forms.IntegerField(label='Enter planet marker size', initial=25)
    symbol_size = forms.IntegerField(label='Enter planet symbol size', initial=15)
    font_size = forms.IntegerField(label='Enter zodiac symbol font size', initial=50)

    line_width = forms.IntegerField(label='Enter axes line width', max_value=7, initial=3)
    house_ax_lw = forms.IntegerField(label='Enter house ax lw', initial=3)
    house_num_fs = forms.IntegerField(label='Enter house number font size', initial=27)
    house_track_lw = forms.IntegerField(label='Enter ht lw', initial=3)


class OneColorZodiacRingFM(forms.ModelForm):

    class Meta:
        model = OneColorZodiacRingMF

        fields = ['chart_name','chart_date', 'chart_mode', 'chart_house_system',
                  'face_color', 'edge_color', 'text_color', 'tick_color',
                  'deg_color', 'marker_color', 'symbol_color',
                  'house_ax_color', 'house_number_color', 'house_track_color',
                  'marker_size','symbol_size', 'font_size',
                  'line_width', 'house_ax_lw','house_num_fs','house_track_lw']

        widgets =  {'chart_date': DateTimePickerInput(),
                    'chart_mode' : Select(),
                    'chart_house_system': Select(),
                    'face_color': ColorWidget(),
                    'edge_color':ColorWidget(),
                    'text_color':ColorWidget(),
                    'tick_color': ColorWidget(),
                    'deg_color' : ColorWidget(),
                    'marker_color': ColorWidget(),
                    'symbol_color' : ColorWidget(),
                    'house_ax_color' : ColorWidget(),
                    'house_number_color': ColorWidget(),
                    'house_track_color': ColorWidget() }

        labels = {'chart_name': 'Enter chart name',
                  'face_color' : 'Enter face color',
                  'edge_color': 'Enter edge color',
                  'text_color': 'Enter text color',
                  'tick_color': 'Enter tick color',
                  'deg_color': 'Enter degrees color',
                  'marker_color': 'Enter marker color',
                  'symbol_color': 'Enter symbol color',
                  'house_ax_color': 'Enter house axes color',
                  'house_number_color': 'Enter house number color',
                  'house_track_color': 'Enter house track color',
                  'chart_date' : 'Enter chart date',
                  'chart_mode': 'Enter chart mode',
                  'chart_house_system': 'Enter house system'}

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


   






