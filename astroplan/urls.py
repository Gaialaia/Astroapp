from django.urls import path
from . import views


urlpatterns = [

    path('show_td_chart/', views.show_td_chart, name='showed chart'),
    path('show_by_date/', views.show_td_chart, name='show by date'),
    path('show_td_chart/show_by_date/', views.show_td_chart, name='show by date'),
    path('chart_form/', views.chart_form, name='form on td chart'),
    path('transit_form/', views.build_transit_chart, name='transit form chart'),
    path('design_your_chart/', views.design_chart, name='design your chart'),
    path('designed_chart/', views.design_chart, name='designed chart')

    # path('today_chart/', views.today_chart, name='td chart'),
    # path('birth_chart/', views.show_birth_chart, name='birth chart'),
    # path('houses_chart/', views.show_chart_houses, name='house axes'),

]