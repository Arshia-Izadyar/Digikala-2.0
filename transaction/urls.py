from django.urls import path
from .views import CreateTransaction, GateWayConfirm


app_name = "transactions"

urlpatterns = [
    path("", CreateTransaction.as_view(), name="create"),
    path("confirm/<uuid:invoice_number>", GateWayConfirm.as_view(), name="confirm"),
]


