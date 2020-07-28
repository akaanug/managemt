# Generated by Django 3.0.8 on 2020-07-23 06:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0018_remove_product_invoice'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='invoice',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='fatura', to='accounts.Invoice'),
        ),
    ]
