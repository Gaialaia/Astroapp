from django.contrib import admin

from .forms import FullChartForm
from .models import Chart, TransitChart, ZodiacInColors, FullChart

# Register your models here.
admin.site.register(Chart)
admin.site.register(TransitChart)
admin.site.register(ZodiacInColors)
admin.site.register(FullChart)
