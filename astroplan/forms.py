from django.forms import DateInput, ModelForm

from .models import Chart
import datetime


from django import forms


class ChartForm(forms.ModelForm):

    class Meta:
        model = Chart
        fields = '__all__'
        widgets = {'chart_date': forms.DateTimeInput(attrs={'type':'datetime.local'})}




