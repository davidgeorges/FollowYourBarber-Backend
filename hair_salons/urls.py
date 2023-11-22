from django.urls import path

from . import views

urlpatterns = [
    path("nearMe", views.get_hair_salons, name="get_hair_salons"),
]