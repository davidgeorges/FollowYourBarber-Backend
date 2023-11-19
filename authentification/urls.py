from django.urls import path
from . import views

urlpatterns = [
    path("login",views.login, name="login"),
    path("logout",views.logout, name="logout"),
    path("register",views.register, name="register"),
    path("get-csrf-token",views.get_csrf_token, name="get-csrf-token"),
]