from django.urls import path
from . import views


urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.custom_login, name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    # path('my_chart/<username>', views.my_chart, name='my chart'),
    path('user_lounge/', views.user_lounge),
    path('user_lounge/<username>', views.user_lounge, name='user lounge'),
    path('user_chart_forms/', views.user_forms, name='ul chart forms')


]