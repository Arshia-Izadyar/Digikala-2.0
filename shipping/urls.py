from django.urls import path

from .views import CreateShipping, ShippingList

app_name = "shipping"

urlpatterns = [
    path("<int:basket_id>/", CreateShipping.as_view(), name="create"),
    path("", ShippingList.as_view(), name="list"),
]