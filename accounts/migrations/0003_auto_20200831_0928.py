# Generated by Django 3.0.8 on 2020-08-31 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20200831_0925'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logs',
            name='type',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]