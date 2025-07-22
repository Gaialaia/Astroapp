from django.forms import DateInput, ModelForm
from django_flatpickr.widgets import DatePickerInput, DateTimePickerInput

from .models import Chart, TransitChart
import datetime


from django import forms


class ChartForm(forms.ModelForm):

    class Meta:
        model = Chart
        fields = '__all__'
        widgets = {
            'chart_date': DateTimePickerInput(attrs={'class':'chart-df','placeholder': 'Chose date',
                                           'style': 'color: rgb(159,0,255) background-color:aliceblue; font-size: x-large;'
                                                    'border-radius: 3px; border: gold;'
                                           }),
            'city': forms.TextInput(attrs={'class':'chart-df','placeholder': 'Enter city',
                                           'style': 'color: rgb(159,0,255) background-color:aliceblue; font-size: x-large;'
                                                    'border-radius: 3px; border: gold; '
                                           }),
            'country': forms.TextInput(attrs={'class':'chart-df','placeholder': 'Enter country',
                                           'style': 'color: rgb(159,0,255) background-color:aliceblue; font-size: x-large;'
                                                    'border-radius: 3px; border: gold; '
                                           }),
        }

class TransitChartForm(forms.ModelForm):

    class Meta:
        style = {'class': 'chart-df','style': 'color: rgb(159,0,255) background-color:aliceblue; font-size: x-large;'
                          'border-radius: 3px; border: gold'}
        model = TransitChart
        fields = '__all__'
        widgets = {'event_date': DateTimePickerInput(attrs= style),
                   'transit_date': DateTimePickerInput(attrs=style),
                   'event_country': forms.TextInput(attrs=style),
                   'transit_country': forms.TextInput(attrs=style),
                   'event_city': forms.TextInput(attrs=style),
                   'transit_city': forms.TextInput(attrs=style),

                   }



