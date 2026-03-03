from django.urls import path
from . import views

urlpatterns = [

    path('register/', views.register, name='register'),
    path('login/', views.custom_login, name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('user_lounge/', views.user_lounge),
    path('user_lounge/<username>', views.user_lounge, name='user lounge'),
    path('user_chart_for_date_form', views.user_chart_for_date_form,
         name='ad user chart'),
    path('user_transit_chart_form', views.user_transit_chart_form,
         name='user tc f'),
    path('user_color_chart_form', views.user_color_chart_form,
         name='user c ch f')
    ]
