from django.contrib import admin
from .models import Chart, TransitChart

# Register your models here.
admin.site.register(Chart)
admin.site.register(TransitChart)