from django.urls import path
from .views import ShowBasket, AddToBasket


app_name = "basket"

urlpatterns = [
    path("", ShowBasket.as_view(), name="show"),
    path("add/", AddToBasket.as_view(), name="add"),
]