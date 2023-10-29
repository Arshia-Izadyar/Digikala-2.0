from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext as _

import uuid

from .managers import CustomUserManager

class User(AbstractUser):
    CONSUMER = 1
    PROVIDER = 2

    user_type =(
        (CONSUMER, "consumer"),
        (PROVIDER, "provider"),
    )
    
    email = models.EmailField(verbose_name=_("Email"), max_length=100, unique=True)
    phone_number = models.CharField(_("Phone number "), max_length=12, unique=True)
    firstname = models.CharField(verbose_name=_("First Name"), max_length=40, blank=False)
    lastname = models.CharField(verbose_name=_("Last Name"), max_length=50)
    score = models.PositiveIntegerField(verbose_name=_("Score"), default=0)
    uuid = models.UUIDField(verbose_name=_("uuid"), default=uuid.uuid4)
    user_type = models.PositiveSmallIntegerField(_("User Type"),choices=user_type, default=CONSUMER)
    birth_date = models.DateField(verbose_name=_("Birth date"), null=True)
    is_staff = models.BooleanField(
        _("Staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )

    is_active = models.BooleanField(
        _("Active"),
        default=True,
        help_text=_("Designates whether this user should be treated as active. "),
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ("firstname", "lastname", "phone_number")

    objects = CustomUserManager()

    def is_provider(self):
        if self.user_type == 2:
            return True
        return False
    
    def __str__(self):
        return self.email

class Address(models.Model):
    user = models.ForeignKey(User, verbose_name=_("User"), on_delete=models.CASCADE, related_name="addresses")
    address = models.TextField(null=False, blank=False)
    zip_code = models.CharField(max_length=14)
    city = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=12)
    receiver_name = models.CharField(max_length=50)
    