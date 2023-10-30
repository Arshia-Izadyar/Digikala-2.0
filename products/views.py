from typing import Any
from django.db.models import Avg, Q
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import FormView, ListView, View, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError
from .forms import ProviderForm, ReviewForm
from .models import Category, Product, ReviewImage, Bookmark

# using a simple view because thats all i need
class CategoryView(View):
    def get(self, request, *args, **kwargs):
        c = Category.objects.all()   
        return render(request, "products/categories.html", {"categories":c})

class ViewPerCategory(ListView):
    
    template_name = "products/product_category.html"    
    context_object_name = "products"
    
    def get_queryset(self):
        slug = self.kwargs["category"]
        search_query = self.request.GET.get('search')
        if search_query:
            return Product.objects.filter(Q(title__icontains=search_query) & Q(category__slug=slug))
        return Product.objects.filter(category__slug=slug)
    
    
class AddBookmark(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        p = self.kwargs["pid"]
        product = Product.objects.get(pid=p)
        try:
            Bookmark.objects.create(user=self.request.user,product=product)
            return redirect(self.request.POST.get("next", "/"))
        except IntegrityError:
            bookmark = Bookmark.objects.filter(Q(product=product) & Q(user= self.request.user)).first()
            bookmark.delete()
            return redirect(self.request.POST.get("next", "/"))
            
    

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


class ProductDetails(DetailView):
    template_name = "products/product_detail.html"
    context_object_name = "product"
    model = Product
    slug_field = "pid"
    slug_url_kwarg = "pid"
    
    def get_queryset(self):
        # queryset = super().get_queryset()
        pid = self.kwargs["pid"]
        product = Product.objects.filter(pid=pid)
        return product
    
    
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        qs = self.get_queryset()
        p = ctx["product"]
        ctx["review_form"] = ReviewForm()
        ctx["reviews"] = p.reviews.all()
        ctx["avg_rate"] = round(sum([i.rating for i in ctx["reviews"]])/len(ctx["reviews"]), 2)
        return ctx


class CreateReview(LoginRequiredMixin, FormView):
    
    def post(self, request, *args, **kwargs) :
        form = ReviewForm(data=request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = self.request.user
            review.product = Product.objects.get(pid=self.kwargs["pid"])
            review.save()
            
            images = request.FILES.getlist("images")
            for image in images:
                ReviewImage.objects.create(review=review, image=image)
                
            return redirect(request.POST.get("next", "/"))
        return redirect(request.POST.get("next", "/"))
    


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
        provider.user = self.request.user
        provider.save()
        return redirect(self.success_url)

