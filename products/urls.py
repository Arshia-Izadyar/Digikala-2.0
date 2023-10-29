from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import CreateProvider, CategoryView, HomeView, ProductDetails, ViewPerCategory, CreateReview

app_name = "product"
# TODO: Add book mark to products
urlpatterns = [
    path("provider/", CreateProvider.as_view(), name="create-provider"),
    path("categories/", CategoryView.as_view(), name="categories"),
    path("categories/<slug:category>", ViewPerCategory.as_view(), name="products_category"),
    path("", HomeView.as_view(), name="home"),
    path("product/<uuid:pid>", ProductDetails.as_view(), name="details"),
    path("product/<uuid:pid>/review", CreateReview.as_view(), name="review"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)