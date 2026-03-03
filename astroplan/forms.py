import swisseph as swe

from django import forms
from django.forms.widgets import TextInput, Select
from django_flatpickr.widgets import DateTimePickerInput
from django.utils import timezone

from .models import (Chart, ZodiacInColors, FullChart, TransitFullChart,
                     OneColorZodiacRingMF)

from colorfield.widgets import ColorWidget
from colorfield.forms import ColorField

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
        PlACIDUS: 'Placidus',
        REGIONMONTANUS: 'Regiomontanus',
        EQUAL: 'Equal',
        'Without houses': 'Without houses',
    }


class ChartForm(forms.ModelForm):
    class Meta:
        model = Chart
        fields = '__all__'
        labels = {'chart_date': 'Enter date', 'city': 'Enter city', 'country': 'Enter country',
                  'chart_mode': 'Chose chart mode', 'house_system': 'Chose house system'}
        widgets = {
            'chart_date': DateTimePickerInput()}

        class Media:
            css = {
                'all': ['/static/styles/form_style.css']
            }


class ShowChart(forms.Form):
    chart_date = forms.DateTimeField(widget=DateTimePickerInput(),
                                     label='Enter date', initial=timezone.now)
    city = forms.CharField(label='Enter city', initial='Ufa')
    country = forms.CharField(label='Enter country', initial='Russia')

    mode = forms.ChoiceField(label='Chose chart mode', choices=MODE_CHOICES,
                             initial='Sidereal', widget=forms.Select)
    house_system = forms.ChoiceField(label='Chose house system',
                                     choices=HOUSE_SYSTEM_CHOICES,
                                     initial='Regiomontanus')

    class Media:
        css = {
            'all': ['/static/styles/form_style.css']
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
                                initial='Sidereal', widget=forms.Select)
    tr_house_system = forms.ChoiceField(label='Chose transit house system',
                                        choices=HOUSE_SYSTEM_CHOICES,
                                        initial='Regiomontanus',
                                        widget=forms.Select)

    class Media:
        css = {
            'all': ['/static/styles/form_style.css']
        }


class FullChartForm(forms.ModelForm):
    class Meta:
        model = FullChart
        fields = ['chart_name', 'chart_date', 'city', 'country', 'chart_mode',
                  'house_system']
        labels = {'chart_name': 'Enter event name',
                  'chart_date': 'Enter date',
                  'city': 'Enter city',
                  'country': 'Enter country',
                  'chart_mode': 'Chose chart mode:',
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
                   'transit_date': DateTimePickerInput()}

        labels = {'event_date': 'Enter an event date',
                  'event_city': 'Enter city',
                  'event_country': 'Enter country',
                  'ev_chart_mode': 'Enter event mode: ',
                  'ev_house_sy stem': 'Enter house system',

                  'transit_date': 'Enter transit date',
                  'transit_city': 'Enter city',
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
    oc_chart_date = (forms.DateTimeField(widget=DateTimePickerInput
                    (attrs={'class': 'form-control',
                            'id': 'chart-date'}),
                    label='Enter chart date', initial=timezone.now))

    oc_chart_city = forms.CharField(label='Enter city', initial='Ufa',
                                    widget=TextInput
                                    (attrs={'class': 'form-control',
                                            'placeholder': 'city',
                                            'id': 'chart-city'}))

    oc_chart_country = forms.CharField(label='Enter country',
                                       widget=TextInput
                                       (attrs={'class': 'form-control',
                                               'id': 'chart-country'}),
                                       initial='Russia')

    one_clr_zr_chart_mode = forms.ChoiceField(label='Chose event chart mode',
                                              choices=MODE_CHOICES,
                                              initial='Sidereal',
                                              widget=forms.Select)
    one_clr_zr_chart_hs = forms.ChoiceField(label='Chose event house system',
                                            choices=HOUSE_SYSTEM_CHOICES,
                                            initial='Regiomontanus')

    face_color = ColorField(widget=ColorWidget
    (attrs={'class': 'form-control', 'id': 'face-color'}),
                            label='Enter face color',
                            initial='#300c63')
    edge_color = ColorField(widget=ColorWidget
    (attrs={'class': 'form-control', 'id': 'edge-color'}), label='Enter edge color',
                            initial='#3dffc8')
    text_color = ColorField(widget=ColorWidget
    (attrs={'class': 'form-control', 'id': 'text-color'}),
                            label='Enter zodiac symbol color',
                            initial='#3dffc8')
    tick_color = ColorField(widget=ColorWidget
    (attrs={'class': 'form-control', 'id': 'tick-color'}),
                            label='Enter tick color',
                            initial='#63ffd3')
    deg_color = ColorField(widget=ColorWidget
    (attrs={'class': 'form-control', 'id': 'deg-color'}),
                           label='Enter degree tick color',
                           initial='#63ffd3')
    marker_color = ColorField(widget=ColorWidget
    (attrs={'class': 'form-control', 'id': 'marker-color'}),
                              label='Enter planet symbol marker color',
                              initial='#ffc83d')
    symbol_color = ColorField(widget=ColorWidget
    (attrs={'class': 'form-control', 'id': 'symbol-color'}),
                              label='Enter planet symbol color',
                              initial='#ff3d74')

    house_ax_color = ColorField(widget=ColorWidget
    (attrs={'class': 'form-control', 'id': 'ha-color'}),
                                label='Enter house ax color',
                                initial='#ffc83d')
    house_number_color = ColorField(widget=ColorWidget
    (attrs={'class': 'form-control', 'id': 'hnum-color'}),
                                    label='Enter house number color',
                                    initial='#ffc83d')
    house_track_color = ColorField(widget=ColorWidget
    (attrs={'class': 'form-control', 'id': 'htr-color'}),
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


class OneColorZodiacRingFM(forms.ModelForm):

    class Meta:

        model = OneColorZodiacRingMF

        fields = ['chart_name', 'chart_date', 'chart_mode', 'chart_house_system',
                  'face_color', 'edge_color', 'text_color', 'tick_color',
                  'deg_color', 'marker_color', 'symbol_color',
                  'house_ax_color', 'house_number_color', 'house_track_color',
                  'marker_size', 'symbol_size', 'font_size',
                  'line_width', 'house_ax_lw', 'house_num_fs', 'house_track_lw']

        widgets = {'chart_date': DateTimePickerInput(),
                   'chart_mode': Select(),
                   'chart_house_system': Select(),
                   'face_color': ColorWidget(),
                   'edge_color': ColorWidget(),
                   'text_color': ColorWidget(),
                   'tick_color': ColorWidget(),
                   'deg_color': ColorWidget(),
                   'marker_color': ColorWidget(),
                   'symbol_color': ColorWidget(),
                   'house_ax_color': ColorWidget(),
                   'house_number_color': ColorWidget(),
                   'house_track_color': ColorWidget()}

        labels = {'chart_name': 'Enter chart name',
                  'face_color': 'Enter face color',
                  'edge_color': 'Enter edge color',
                  'text_color': 'Enter text color',
                  'tick_color': 'Enter tick color',
                  'deg_color': 'Enter degrees color',
                  'marker_color': 'Enter marker color',
                  'symbol_color': 'Enter symbol color',
                  'house_ax_color': 'Enter house axes color',
                  'house_number_color': 'Enter house number color',
                  'house_track_color': 'Enter house track color',
                  'chart_date': 'Enter chart date',
                  'chart_mode': 'Enter chart mode',
                  'chart_house_system': 'Enter house system'}

    class Media:
        css = {
            'all': ['/static/styles/form_style.css']
        }
