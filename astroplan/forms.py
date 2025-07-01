from django.forms import DateInput, ModelForm
from django_flatpickr.widgets import DatePickerInput, DateTimePickerInput

from .models import Chart, TransitChart
import datetime


from django import forms


class ChartForm(forms.ModelForm):

    class Meta:
        model = Chart
        fields = '__all__'
        widgets = {'chart_date': DateTimePickerInput()}

class TransitChartForm(forms.ModelForm):

    class Meta:

        model = TransitChart
        fields = '__all__'
        widgets = {'event_date': DateTimePickerInput(),
                   'transit_date': DateTimePickerInput()}



