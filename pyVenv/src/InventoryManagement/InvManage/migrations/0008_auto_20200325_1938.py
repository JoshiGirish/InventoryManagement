# Generated by Django 3.0.4 on 2020-03-25 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('InvManage', '0007_product_expiry'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
