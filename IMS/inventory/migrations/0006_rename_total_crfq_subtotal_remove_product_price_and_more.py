# Generated by Django 5.0.1 on 2024-02-12 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0005_crfq_notes_crfq_status_crfq_total'),
    ]

    operations = [
        migrations.RenameField(
            model_name='crfq',
            old_name='total',
            new_name='subtotal',
        ),
        migrations.RemoveField(
            model_name='product',
            name='price',
        ),
        migrations.AddField(
            model_name='crfq',
            name='desc',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='crfq',
            name='tax',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='crfq',
            name='taxamt',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='crfq',
            name='taxval',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='crfq',
            name='tcs',
            field=models.CharField(choices=[('KG', 'KG'), ('Gram', 'Gram'), ('Unit', 'Unit')], max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='crfq',
            name='tcsval',
            field=models.IntegerField(null=True),
        ),
    ]
