from django.forms import DateInput, ModelForm
from django_flatpickr.widgets import DatePickerInput, DateTimePickerInput

from .models import Chart, TransitChart
import datetime


from django import forms


class ChartForm(forms.ModelForm):
    class Meta:
        model = Chart
        fields = '__all__'
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


class TransitChartForm(forms.ModelForm):

    class Meta:
        model = TransitChart
        fields = '__all__'

        class Media:
            css = {
                'all': ['/static/styles/form_style.css']
            }
        widgets = {'event_date': DateTimePickerInput(),
                   'transit_date': DateTimePickerInput()
                   }
        labels = {'event_date': 'Enter an event date',
                  'event_city': 'Enter city',
                  'event_country': 'Enter country',
                  'transit_date': 'Enter transit date',
                  'transit_city':  'Enter city',
                  'transit_country': 'Enter country',

                  }






