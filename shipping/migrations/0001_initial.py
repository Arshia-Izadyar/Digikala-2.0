# Generated by Django 4.2 on 2023-11-08 09:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import utils.rate_validator


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
        ('products', '0003_alter_bookmark_unique_together'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Shipping',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sending_date', models.DateField(validators=[utils.rate_validator.validated_date], verbose_name='Shipping Date')),
                ('delivery_method', models.PositiveSmallIntegerField(choices=[(1, 'digikala plus'), (2, 'digikala express'), (3, 'Provider')], default=2, verbose_name='Delivery method')),
                ('is_deliverd', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_shipping', to=settings.AUTH_USER_MODEL, verbose_name='User')),
                ('user_address', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='shippings', to='accounts.address', verbose_name='User Address')),
            ],
        ),
        migrations.CreateModel(
            name='ShippingItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1, verbose_name='quantity')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shipping_line', to='products.product', verbose_name='Product')),
                ('shipping', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shipping_line', to='shipping.shipping', verbose_name='Shipping')),
            ],
        ),
    ]