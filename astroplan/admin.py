from django.contrib import admin
from .models import (Chart, TransitChart, ZodiacInColors, FullChart,
                     TransitFullChart, OneColorZodiacRingMF)


admin.site.register(Chart)
admin.site.register(TransitChart)
admin.site.register(ZodiacInColors)
admin.site.register(FullChart)
admin.site.register(TransitFullChart)
admin.site.register(OneColorZodiacRingMF)
