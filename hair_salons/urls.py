from django.urls import path

from . import views

urlpatterns = [
    path("", views.get_hair_salons, name="get_hair_salons"),
    path("<int:hair_salon_id>/", views.get_hair_salon, name="get_hair_salon"),
]