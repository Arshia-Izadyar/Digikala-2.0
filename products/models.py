from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

from uuid import uuid4
from utils import rate_validator
User = get_user_model()



class Category(models.Model):
    title = models.CharField(max_length=40)
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = _("Categories")

    def __str__(self):
        return self.title


class Provider(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    provider_name = models.CharField(max_length=50, unique=True)
    joined = models.DateField(auto_now_add=True)
    address = models.TextField()
    working_perm_id = models.CharField(max_length=14, unique=True)
    owner_national_code = models.CharField(max_length=15, unique=True)
    location = models.CharField(max_length=40, null=True)
    def __str__(self):
        return self.provider_name
    
    # performance = models
    
    
class Product(models.Model):
    title = models.CharField(_("Title"), max_length=120, unique=True)
    pid = models.UUIDField(_("Pid"), default=uuid4, unique=True)
    description = models.TextField()
    price = models.DecimalField(verbose_name=_("Price") , max_digits=10, decimal_places=2)
    in_digikala_inventory = models.BooleanField(default=False)
    in_provider_inventory = models.BooleanField(default=True)
    provider = models.ManyToManyField(Provider)
    category = models.ForeignKey(Category, verbose_name=_("Category"), on_delete=models.PROTECT)
    
    
    def __str__(self):
        return self.title
    

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='images/')

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    rating = models.PositiveIntegerField(validators=[rate_validator.validate_rate]) 
    review = models.TextField(blank=True, null=True)
    created_date = models.DateField(auto_now_add=True)
    recommend = models.BooleanField(default=True)
    is_anon = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.product} - {self.user}"
    
    
class ProductImage(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='images/')

