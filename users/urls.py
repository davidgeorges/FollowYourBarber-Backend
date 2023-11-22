from django.urls import path

from . import views

urlpatterns = [
    path("accountDetails", views.get_account_details, name="get_account_details"),
]