from django.urls import path
from . import views


urlpatterns = [
    path('chart/', views.chart, name='chart'),
    path('show_chart/', views.show_chart, name='showed chart'),
    path('transit_chart/', views.show_transit_chart, name='transit chart'),
    path('birth_chart/', views.show_birth_chart, name='birth chart')
]
