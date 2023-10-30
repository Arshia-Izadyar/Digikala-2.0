# from django.db import models

# from django.contrib.auth import get_user_model
# from django.utils.translation import gettext_lazy as _
# from uuid import uuid4

# User = get_user_model()


# class Transactions(models.Model):
#     PAID = 10
#     PENDING = 0 
#     NOT_PAID = -10
    
#     transaction_status = (
#             (PAID, _("paid")),
#             (PENDING,_("pending")),
#             (NOT_PAID, _("Not paid")),
#             )
    
    
#     PURCHASE = 1
#     CHARGE = 2
    
#     transaction_type = (
#         (PURCHASE, _("purchase")),
#         (CHARGE, _("charge")),
#     )
    
#     user = models.ForeignKey(User, on_delete=models.SET("deleted_user"), related_name="transactions", verbose_name=_("User"))
#     amount = models.DecimalField(max_digits=15, decimal_places=2, verbose_name=_("Amount"))
#     type = models.PositiveSmallIntegerField(choices=transaction_type, default=PURCHASE)
#     created_at = models.DateTimeField(auto_now_add=True)
#     invoice_number = models.UUIDField(default=uuid4, verbose_name=_("Invoice number"))
    