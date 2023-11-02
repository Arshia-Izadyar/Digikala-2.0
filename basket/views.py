from typing import Any
from django.shortcuts import render
from django.views.generic import View, TemplateView
from django.http import HttpResponseRedirect, Http404

from basket.models import Basket
from .forms import AddToBasketForm


class AddToBasket(View):
    def post(self, request, *args, **kwargs):
        response = HttpResponseRedirect(self.request.POST.get("next", "/"))
        basket_id = request.COOKIES.get("basket_id", None)
        basket = Basket.get_basket(basket_id)
        if basket is None:
            raise Http404
        response.set_cookie("basket_id", basket.pk)
        
        if not basket.user_validate(self.request.user):
            raise Http404
        form = AddToBasketForm(request.POST)
        if form.is_valid():
 
            form.save_to_basket(basket)
        
        return response
    

class ShowBasket(TemplateView):
    model = Basket
    template_name = "basket/basket_view.html"
    
    def get(self, request, *args, **kwargs):
        
        if not hasattr(self, "basket_object"):
            
            id = self.request.COOKIES.get("basket_id", None)
            self.basket_object = Basket.get_basket(id)

            if not self.basket_object.user_validate(self.request.user):
                raise Http404
        
        context = self.get_context_data()
        response = render(request, "basket/basket_view.html", context)
        response.set_cookie("basket_id", self.basket_object.pk)
        return response
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        ctx = super().get_context_data(**kwargs)
        lines = self.basket_object.lines.all()
        ctx["total"] = sum([line.product.price * line.quantity for line in lines])
        ctx["lines"] = lines
        ctx["basket"] = self.basket_object
        return ctx

def basket_merge_after_login(user, request):
    authenticated_basket = Basket.objects.filter(user=user, is_paid=False).first()
    id = request.COOKIES.get("basket_id", None)
    session_basket = Basket.get_basket(id)
    if authenticated_basket and session_basket:
        for line in session_basket.lines.all():
            authenticated_basket.add_to_basket(line.product, line.quantity)
        session_basket.delete()
    
    return authenticated_basket
    
    