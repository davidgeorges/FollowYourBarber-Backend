from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('auth/', include('authentification.urls')),
    path('hairDressers/', include('hairdressers.urls')),
    path('managers/', include('managers.urls')),
    path('hairSalons/', include('hair_salons.urls')),
]  
