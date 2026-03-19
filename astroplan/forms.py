import swisseph as swe

from django import forms
from django.forms.widgets import TextInput, Select
from django_flatpickr.widgets import DateTimePickerInput
from django.utils import timezone

from colorfield.widgets import ColorWidget
from colorfield.forms import ColorField

SIDEREAL = swe.FLG_SIDEREAL
TROPICAL = swe.FLG_TROPICAL
HELIOCENTRIC = swe.FLG_HELCTR


MODE_CHOICES = {
        SIDEREAL : 'Sidereal',
        TROPICAL : 'Tropical',
        HELIOCENTRIC : 'Heliocentric',
        }

PlACIDUS = 'P'
REGIONMONTANUS = 'R'
EQUAL = 'E'

HOUSE_SYSTEM_CHOICES = \
    {
        PlACIDUS : 'Placidus',
        REGIONMONTANUS : 'Regiomontanus',
        EQUAL :  'Equal',
        'Without houses' : 'Without houses',
    }


class ShowChart(forms.Form):

    chart_date = forms.DateTimeField(widget=DateTimePickerInput(),
                                     label='Enter date', initial=timezone.now)
    city = forms.CharField(label='Enter city', initial='Ufa')
    country = forms.CharField(label='Enter country', initial='Russia')

    mode = forms.ChoiceField(label = 'Chose chart mode', choices=MODE_CHOICES,
                             initial='Sidereal', widget=forms.Select)
    house_system = forms.ChoiceField(label='Chose house system',
                                     choices=HOUSE_SYSTEM_CHOICES,
                                     initial='Regiomontanus')

    class Media:
        css = {
            'all' : ['/static/styles/form_style.css']
        }


class TransitForm(forms.Form):

    event_date = forms.DateTimeField(widget=DateTimePickerInput(),
                                     label='Enter event date', initial=timezone.now)
    event_city = forms.CharField(label='Enter event city', initial='Ufa')
    event_country = forms.CharField(label='Enter event country', initial='Russia')

    ev_mode = forms.ChoiceField(label='Chose event chart mode', choices=MODE_CHOICES,
                                initial='Sidereal', widget=forms.Select)
    ev_house_system = forms.ChoiceField(label='Chose event house system',
                                        choices=HOUSE_SYSTEM_CHOICES,
                                        initial='Regiomontanus',
                                        widget=forms.Select)

    transit_date = forms.DateTimeField(widget=DateTimePickerInput(),
                                       label='Enter transit date')
    transit_city = forms.CharField(label='Enter transit city', initial='Ufa')
    transit_country = forms.CharField(label='Enter transit country', initial='Russia')

    tr_mode = forms.ChoiceField(label='Chose transit chart mode', choices=MODE_CHOICES,
                                initial='Sidereal',widget=forms.Select)
    tr_house_system = forms.ChoiceField(label='Chose transit house system',
                                        choices=HOUSE_SYSTEM_CHOICES,
                                        initial='Regiomontanus',
                                        widget=forms.Select)
    class Media:
        css = {
            'all': ['/static/styles/form_style.css']
        }

class OneColorZodiacRing(forms.Form):

    oc_chart_date = (forms.DateTimeField
                     (widget=DateTimePickerInput
                     (attrs={'class' : 'form-control',
                            'id' : 'chart-date'}),
                      label='Enter chart date',
                      initial=timezone.now))
    oc_chart_city = forms.CharField(label='Enter city', initial='Ufa',
                                    widget=TextInput(attrs={'class' : 'form-control',
                                                            'placeholder' : 'city',
                                                            'id' : 'chart-city'}))
    oc_chart_country = forms.CharField(label='Enter country',
                                       widget=TextInput
                                       (attrs={'class' : 'form-control',
                                               'id' : 'chart-country'}),
                                       initial='Russia')

    one_clr_zr_chart_mode = forms.ChoiceField(label='Chose event chart mode',
                                              choices=MODE_CHOICES,
                                              initial='Sidereal',
                                              widget=forms.Select)
    one_clr_zr_chart_hs = forms.ChoiceField(label='Chose event house system',
                                            choices=HOUSE_SYSTEM_CHOICES,
                                            initial='Regiomontanus')

    face_color = ColorField(widget=ColorWidget
    (attrs={'class': 'form-control', 'id'  : 'face-color'}),
                            label='Enter face color',
                            initial='#300c63')
    edge_color = ColorField(widget=ColorWidget
    (attrs={'class': 'form-control', 'id' : 'edge-color'}),
                            label='Enter edge color',
                            initial='#3dffc8')
    text_color = ColorField(widget=ColorWidget
    (attrs={'class': 'form-control', 'id' : 'text-color'}),
                            label='Enter zodiac symbol color',
                            initial='#3dffc8')
    tick_color = ColorField(widget=ColorWidget
    (attrs={'class': 'form-control',  'id' : 'tick-color'}),
                            label='Enter tick color',
                            initial='#63ffd3')
    deg_color = ColorField(widget=ColorWidget
    (attrs={'class': 'form-control', 'id' : 'deg-color'}),
                           label='Enter degree tick color',
                           initial='#63ffd3')
    marker_color = ColorField(widget=ColorWidget
    (attrs={'class': 'form-control', 'id' : 'marker-color'}),
                              label='Enter planet symbol marker color',
                              initial='#ffc83d')
    symbol_color = ColorField(widget=ColorWidget
    (attrs={'class': 'form-control', 'id' : 'symbol-color'}),
                            label='Enter planet symbol color',
                            initial='#ff3d74')

    house_ax_color = ColorField(widget=ColorWidget
    (attrs={'class': 'form-control', 'id' : 'ha-color'}),
                                label='Enter house ax color',
                                initial='#ffc83d')
    house_number_color = ColorField(widget=ColorWidget
    (attrs={'class': 'form-control', 'id' : 'hnum-color'}),
                                    label='Enter house number color',
                                    initial='#ffc83d')
    house_track_color = ColorField(widget=ColorWidget
    (attrs={'class': 'form-control', 'id' : 'htr-color'}),
                            label='Enter house track color',
                                   initial='#ffc83d')

    marker_size = forms.IntegerField(label='Enter planet marker size',
                                     initial=25)
    symbol_size = forms.IntegerField(label='Enter planet symbol size',
                                     initial=15)
    font_size = forms.IntegerField(label='Enter zodiac symbol font size',
                                   initial=50)
    line_width = forms.IntegerField(label='Enter axes line width', max_value=7,
                                    initial=3)
    house_ax_lw = forms.IntegerField(label='Enter house ax lw',
                                     initial=3)
    house_num_fs = forms.IntegerField(label='Enter house number font size',
                                      initial=27)
    house_track_lw = forms.IntegerField(label='Enter ht lw',
                                        initial=3)











