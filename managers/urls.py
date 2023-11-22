from django.urls import path

from . import views

urlpatterns = [
    path("employees", views.get_employees, name="get_employees"),
]