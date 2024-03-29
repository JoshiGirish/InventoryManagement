# Generated by Django 2.2.12 on 2020-04-05 18:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('InvManage', '0014_auto_20200404_2343'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='ppentries',
        ),
        migrations.RemoveField(
            model_name='productpurchaseentry',
            name='identifier',
        ),
        migrations.RemoveField(
            model_name='productpurchaseentry',
            name='subtotal',
        ),
        migrations.AddField(
            model_name='productpurchaseentry',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='InvManage.Product'),
        ),
    ]
