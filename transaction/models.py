from django.db import models, transaction
from django.db.models.functions import Coalesce
from django.db.models import Sum, Q, DecimalField

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _

from uuid import uuid4
from basket.models import Basket

User = get_user_model()


class Transactions(models.Model):
    PAID = 10
    PENDING = 0 
    NOT_PAID = -10
    
    transaction_status = (
            (PAID, _("paid")),
            (PENDING,_("pending")),
            (NOT_PAID, _("Not paid")),
            )
    
    
    PURCHASE = 1
    CHARGE = 2
    
    transaction_type = (
        (PURCHASE, _("purchase")),
        (CHARGE, _("charge")),
    )
    
    user = models.ForeignKey(User, on_delete=models.SET("deleted_user"), related_name="transactions", verbose_name=_("User"))
    amount = models.DecimalField(max_digits=15, decimal_places=2, verbose_name=_("Amount"))
    type = models.PositiveSmallIntegerField(choices=transaction_type, default=PURCHASE)
    created_at = models.DateTimeField(auto_now_add=True)
    invoice_number = models.UUIDField(default=uuid4, verbose_name=_("Invoice number"))
    basket = models.ForeignKey(Basket, on_delete=models.SET("deleted basket"), related_name="transactions",null=True,blank=True, verbose_name=_("Basket"))
    
    def __str__(self):
        return f"{self.user} - {self.type} - {self.amount}"
    
    @classmethod
    def get_user_report(cls, email):
        positive = Sum("transactions__amount", filter=Q(transactions__type=Transactions.CHARGE))
        negative = Sum("transactions__amount", filter=Q(transactions__type=Transactions.PURCHASE))
        total = User.objects.filter(email=email).aggregate(
                sum=Coalesce(positive, 0, output_field=DecimalField(15, 2)) - Coalesce(negative, 0, output_field=DecimalField(15, 2)))
        return total["sum"]
    
    @classmethod
    def purchase(cls, user, amount, basket):
        if cls.get_user_report >= amount:
            return cls.objects.create(user=user, amount=amount, type=Transactions.PURCHASE, basket=basket)
        else:
            raise ValidationError("user cant transfer")
    
    @classmethod
    def calc_user_score(cls, email):
        with transaction.atomic():
            u = User.objects.select_for_update().get(email=email)
            total = User.objects.filter(email=email).aggregate(total=Sum("transactions__amount", filter=Q(transactions__type=Transactions.PURCHASE)))["total"]
            
            if total is None:
                score = 0
            else:
                score = (total // 10_000) * 5
            u.score = score
            print(u.score)
            
            u.save()
            return u.score
    
    
class Wallet(models.Model):
    user = models.OneToOneField(User, related_name="wallet", on_delete=models.CASCADE)
    total = models.PositiveBigIntegerField(default=0, verbose_name=_("Total"))
    
    @classmethod
    def update_wallet(cls, user):
        with transaction.atomic():
            try:
                obj = cls.objects.select_for_update().get(user=user)
            except ObjectDoesNotExist:
                obj = cls.objects.create(user=user)
            total = Transactions.get_user_report(user.email)
            if total is not None:
                obj.total = total
            else:
                obj.total = 0
            obj.save()