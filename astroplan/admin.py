from django.contrib import admin
from .models import Chart, TransitChart, ZodiacInColors

# Register your models here.
admin.site.register(Chart)
admin.site.register(TransitChart)
admin.site.register(ZodiacInColors)