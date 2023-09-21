from django.urls import path

from . import views

from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
    path("", views.index, name="index"),
    # login-section
    path("login/",  views.user_login, name="login-user"),
    #path("login/", LoginView.as_view
         #(template_name="chat/login.html"), name="login-user"),
    path("logout/", LogoutView.as_view(), name="logout-user"),
    path("chat/start/", views.chat_start, name="chat-start"),
    path("chat/send/", views.chat_send, name="chat-send"),
    path("online-users/", views.get_online_users, name="online-users"),
    path("register/", views.register, name="register"),
]
