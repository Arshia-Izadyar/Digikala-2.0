from typing import Any
from django.db import models
from django.db.models import Avg
from django.http import Http404, HttpRequest, HttpResponse, HttpResponseForbidden
from django.shortcuts import redirect, render
from django.views.generic import FormView, ListView, View, DetailView


from .forms import ProviderForm
from .models import Category, Product

# using a simple view because thats all i need
class CategoryView(View):
    def get(self, request, *args, **kwargs):
        c = Category.objects.all()   
        return render(request, "products/categories.html", {"categories":c})
    

class HomeView(ListView):
    context_object_name = "products"
    template_name = "products/home.html"
    
    def get_queryset(self):
        queryset = Product.objects.all()
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category=category)
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(title__icontains=search_query)
        if not search_query and not category:
            # returning top products if user is not searching for a specific product
            queryset = Product.objects.annotate(avg_rating=Avg('reviews__rating')).filter(avg_rating__gt=3)
        return queryset
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        ctx = super().get_context_data(**kwargs)
        ctx["categories"] = Category.objects.all()  
        return ctx


class ProductDetails(View):
    template_name = "products/product_detail.html"
    context_object_name = "product"
    
    def get(self, request, *args, **kwargs):
        pid = self.kwargs["pid"]
        product = Product.objects.get(pid=pid)
        
        return render(request, self.template_name, {self.context_object_name:product})
    
class CreateProvider(FormView):
    template_name = "products/create_provider.html"
    success_url = "/"
    form_class = ProviderForm
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_provider():
            
            return super().dispatch(request, *args, **kwargs)
        return redirect('/')
    
    def form_valid(self, form: Any) -> HttpResponse:
        provider = form.save(commit=False)
        provider.User = self.request.user
        provider.save()
        return redirect(self.success_url)
