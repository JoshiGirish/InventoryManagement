# Generated by Django 2.2.12 on 2020-07-12 07:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('InvManage', '0032_productsalesentry_salesorder'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productsalesentry',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='InvManage.SalesOrder'),
        ),
    ]
