from typing import Any
from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect
from django.views.generic import TemplateView, View
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin


from .models import Transactions
from basket.models import Basket



class CreateTransaction(LoginRequiredMixin, View):
    template_name = "transactions/create_transaction.html"
    
    
    def get(self, request, *args, **kwargs):
        basket_id = self.request.COOKIES.get("basket_id", None)
        if basket_id is None:
            return HttpResponseRedirect("/")
        self.basket = Basket.get_basket(basket_id)
        total = sum([i.product.price * i.quantity for i in self.basket.lines.all()])
        lines = [i for i in self.basket.lines.all()]
        
        if Transactions.objects.filter(Q(user=self.request.user) & Q(status=Transactions.PENDING)).exists() and total > 0:
            transaction = Transactions.objects.get(Q(user=self.request.user) & Q(status=Transactions.PENDING))
            transaction.amount = total
            transaction.basket = self.basket
            transaction.save()
            self.basket.lines.all().delete()
            return render(request, self.template_name, {"basket":self.basket, "lines":lines, "total":total, "transaction":transaction})
        else:
            if total > 0:
                transaction = Transactions.objects.create(user=request.user, amount=total, status=Transactions.PENDING, basket=self.basket, type=Transactions.PURCHASE)
                self.basket.lines.all().delete()
                
                return render(request, self.template_name, {"basket":self.basket, "lines":lines, "total":total, "transaction":transaction})

        raise Http404
            
        



class GateWayConfirm(LoginRequiredMixin, View):
    # i dont have payment gateway so we skip the payment in gateway
    # we assume that the program claimed th transaction from gateway
    template_name = "transactions/confirm_transaction.html"

    def get(self, request, invoice_number):
        transaction = Transactions.objects.get(invoice_number=invoice_number)
        if request.user == transaction.user:
            transaction.status = Transactions.PAID
            transaction.basket.is_paid = True
            transaction.save()
        else:
            raise Http404

        return render(request, self.template_name, {"transaction": transaction})