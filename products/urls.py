from django.urls import path
from .views import CreateProvider, CategoryView, HomeView, ProductDetails, ViewPerCategory, CreateReview, AddBookmark

app_name = "product"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("provider/", CreateProvider.as_view(), name="create-provider"),
    
    path("product/<uuid:pid>", ProductDetails.as_view(), name="details"),
    path("product/bookmark/<uuid:pid>", AddBookmark.as_view(), name="bookmark"),
    path("product/<uuid:pid>/review", CreateReview.as_view(), name="review"),
    
    path("categories/<slug:category>", ViewPerCategory.as_view(), name="products_category"),
    path("categories/", CategoryView.as_view(), name="categories"),
]
