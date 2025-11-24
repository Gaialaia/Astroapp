from django.urls import path
from . import views


urlpatterns = [
    path('show_td_chart/', views.show_td_chart, name='showed chart'),
    path('show_td_chart/show_by_date/', views.show_td_chart, name='show by date'),
    path('chart_form/', views.chart_form, name='form on td chart'),
    path('transit_form/', views.build_transit_chart, name='transit form chart'),
    path('chart/<id>/', views.chart_detail),
    path('tr_chart/<id>/', views.tr_chart_detail),
    path('clr_chart/<id>/', views.clr_chart_detail),
    path('design_one_clr_ch/', views.one_color_chart, name='color your chart'),
    path('designed_oc_chart/', views.one_color_chart, name='colored chart'),
    path('user_chart_lists/', views.user_chart_lists, name='user chart lists'),
    path('chart_for_any_date/', views.chart_for_any_date, name='chart for ad')
]