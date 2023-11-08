from typing import Any, Dict
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.shortcuts import redirect

from django.views.generic import FormView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import ShippingForm
from .models import Shipping
from basket.models import Basket


class CreateShipping(LoginRequiredMixin, FormView):
    form_class = ShippingForm
    template_name = "shipping/add_shipping.html"
    
    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        if len(self.request.user.addresses.all()) == 0:
            return HttpResponseRedirect(reverse_lazy("accounts:address-create"))
        return super().get(request, *args, **kwargs)
    
    def get_form_kwargs(self):
        
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        shipping = form.save(commit=False)
        shipping.user = self.request.user
        shipping.save()
        basket_id = self.kwargs["basket_id"]
        basket = Basket.get_basket(basket_id)
        basket.add_to_shipping(shipping)
        # basket.lines.all().delete()
        return redirect(reverse_lazy("transactions:create"))


class ShippingList(LoginRequiredMixin, ListView):
    template_name = "shipping/shipping_list.html"
    context_object_name = "shippings"

    def get_queryset(self):
        return Shipping.objects.prefetch_related("shipping_line").filter(user=self.request.user, is_deliverd=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        shipping_items = context["shippings"]
        products = []
        for shipping in shipping_items:
            products.extend(shipping.shipping_line.all())
        context["products"] = products
        return context