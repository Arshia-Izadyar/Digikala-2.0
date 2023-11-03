from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
# Create your views here.

from basket.models import Basket


class CreateTransaction(TemplateView):
    template_name = "transactions/create_transaction.html"
    
    # TODO: finish this part and add shipping
    def get(self, request, *args, **kwargs):
        basket_id = self.request.COOKIES.get("basket_id", None)
        if basket_id is None:
            return HttpResponseRedirect("/")
        basket = Basket.get_basket(basket_id)
        print(basket)
        