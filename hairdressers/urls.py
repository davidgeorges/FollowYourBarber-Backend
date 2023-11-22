from django.urls import path

from . import views

urlpatterns = [
    path("schedule", views.get_schedule, name="get_schedule"),
]