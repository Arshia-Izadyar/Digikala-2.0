from django.urls import path

from .views import LoginUser, LogoutUser, CreateUser, Profile, CreateAddress, ListAddress, UpdateAddress, DeleteAddress
# TODO: add reset password

app_name = "accounts"



urlpatterns = [
    path("login/", LoginUser.as_view(), name="login"),
    path("logout/", LogoutUser.as_view(), name="logout"),
    path("sign-up/", CreateUser.as_view(), name="signin"),
    path("profile/", Profile.as_view(), name="profile"),
    path("address/create", CreateAddress.as_view(), name="address-create"),
    path("address/list", ListAddress.as_view(), name="address-list"),
    path("address/update/<int:id>", UpdateAddress.as_view(), name="address-update"),
    path("address/delete/<int:id>", DeleteAddress.as_view(), name="address-delete"),
]