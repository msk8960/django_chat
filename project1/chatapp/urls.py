from django.urls import path

from . import views

from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
    path("", views.index, name="index"),
    # login-section
    path("login/", LoginView.as_view
         (template_name="chat/LoginPage.html"), name="login-user"),
    path("logout/", LogoutView.as_view(), name="logout-user"),
    path("register/", views.register, name="register"),
]
