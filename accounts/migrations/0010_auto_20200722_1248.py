# Generated by Django 3.0.8 on 2020-07-22 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_auto_20200722_1245'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='dateBought',
            field=models.DateTimeField(null=True),
        ),
    ]