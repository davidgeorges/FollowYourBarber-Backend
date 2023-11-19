from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('auth/', include('authentification.urls')),
    path('hairdressers/', include('hairdressers.urls')),
    path('managers/', include('managers.urls')),
    path('hair_salons/', include('hair_salons.urls')),
]  
