from django.db import models

from django.contrib.auth import get_user_model
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from products.models import Product
User = get_user_model()


class Basket(models.Model):
    user = models.ForeignKey(User, verbose_name=_("User"), on_delete=models.CASCADE, related_name="basket", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)
    
    def add_to_basket(self, product, amount=1):
        line, created = self.lines.get_or_create(product=product, defaults={"quantity": int(amount)})
        if not created:
            line.quantity += int(amount)
            line.save()
        return line
    
    def remove_from_basket(self, product):
        line, created = self.lines.get_or_create(product=product)
        if not created:
            line.quantity -= 1
        if line.quantity == 0:
            line.delete()
        else:    
            line.save()
        return line
    
    def user_validate(self, user):      # Validate user that requested the basket 
        if user.is_authenticated:
            if self.user is not None and self.user != user:
                return False
            if self.user is None:
                self.user = user
                self.save()
        elif self.user is not None:
            return False
        return True
    
    @classmethod
    def get_basket(cls, basket_id):
        if basket_id is None:
            basket = cls.objects.create()
        else:
            try:
                basket = cls.objects.filter(Q(pk=basket_id) & Q(is_paid=False)).first()
            except cls.DoesNotExist:
                basket = None
        return basket
    
    def __str__(self):
        return f"{self.user} - {self.created_at} - {self.is_paid}"
    
class BasketLine(models.Model):     
    quantity = models.PositiveSmallIntegerField(_("Quantity"), default=1)
    product = models.ForeignKey(Product, verbose_name=_("Product"), on_delete=models.CASCADE, related_name="lines")
    basket = models.ForeignKey(Basket, verbose_name=_("Basket"), on_delete=models.CASCADE, related_name="lines")
    
    def __str__(self):
        return f"{self.product} - {self.basket} - {self.quantity}"