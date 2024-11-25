# Generated by Django 5.0.1 on 2024-02-14 16:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0010_remove_crfq_desc_remove_crfq_order_quantity_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='crfq',
            name='subtotal',
        ),
        migrations.AddField(
            model_name='crfq',
            name='desc',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='crfq',
            name='order_quantity',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='crfq',
            name='price',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='crfq',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='inventory.product'),
        ),
        migrations.AddField(
            model_name='crfq',
            name='uom',
            field=models.CharField(choices=[('KG', 'KG'), ('Gram', 'Gram'), ('Unit', 'Unit')], max_length=10, null=True),
        ),
        migrations.DeleteModel(
            name='LineItem',
        ),
    ]
