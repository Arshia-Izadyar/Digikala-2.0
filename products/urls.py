from django.urls import path
from .views import CreateProvider, CategoryView, HomeView, ProductDetails

app_name = "product"

urlpatterns = [
    path("provider/", CreateProvider.as_view(), name="create-provider"),
    path("categories/", CategoryView.as_view(), name="categories"),
    path("", HomeView.as_view(), name="home"),
    path("product/<uuid:pid>", ProductDetails.as_view(), name="details"),
]