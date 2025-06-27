from django.forms import DateInput, ModelForm
from django_flatpickr.widgets import DatePickerInput, DateTimePickerInput

from .models import Chart
import datetime


from django import forms


class ChartForm(forms.ModelForm):

    class Meta:
        model = Chart
        fields = '__all__'
        widgets = {'chart_date': DateTimePickerInput()}




