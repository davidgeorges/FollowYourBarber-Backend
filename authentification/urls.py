from django.urls import path
from . import views

urlpatterns = [
    path("login",views.login, name="login"),
    path("logout",views.logout, name="logout"),
    path("register",views.register, name="register"),
    path("sendVerificationMail/<int:user_id>",views.send_verification_mail, name="send_verification_mail"),
    path("refreshToken",views.refresh_token, name="refresh_token"),
    path("get-csrf-token",views.get_csrf_token, name="get-csrf-token"),
]