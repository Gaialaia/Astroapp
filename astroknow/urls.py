from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings
from astroplan.urls import views

urlpatterns = [

    path('', include('astroplan.urls')),
    path('', views.show_td_chart),
    path('admin/', admin.site.urls),
    path("", include('users.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)