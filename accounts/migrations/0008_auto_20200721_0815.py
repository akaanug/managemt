# Generated by Django 3.0.8 on 2020-07-21 08:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_auto_20200721_0813'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='regDate',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]