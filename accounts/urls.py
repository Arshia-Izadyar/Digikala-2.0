from django.urls import path

from .views import LoginUser, LogoutUser, CreateUser


app_name = "accounts"



urlpatterns = [
    path("login/", LoginUser.as_view(), name="login"),
    path("logout/", LogoutUser.as_view(), name="logout"),
    path("sign-up/", CreateUser.as_view(), name="signin"),
]