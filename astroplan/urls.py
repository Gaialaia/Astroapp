from django.urls import path
from . import views


urlpatterns = [
    path('chart/', views.chart, name='chart'),
    path('show_chart/', views.show_chart, name='showed chart'),
]
