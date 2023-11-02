# Generated by Django 4.2 on 2023-11-02 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basket', '0001_initial'),
        ('transaction', '0002_alter_transactions_basket'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transactions',
            name='basket',
            field=models.ForeignKey(blank=True, null=True, on_delete=models.SET('deleted basket'), related_name='transactions', to='basket.basket', verbose_name='Basket'),
        ),
    ]
