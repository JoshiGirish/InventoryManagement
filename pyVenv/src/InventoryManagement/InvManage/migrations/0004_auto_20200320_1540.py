# Generated by Django 3.0.3 on 2020-03-20 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('InvManage', '0003_product_discount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='quantity',
            field=models.IntegerField(default=0, null=True),
        ),
    ]