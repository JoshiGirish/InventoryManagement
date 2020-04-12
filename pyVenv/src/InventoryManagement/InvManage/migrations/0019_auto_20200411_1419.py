# Generated by Django 2.2.12 on 2020-04-11 08:49

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('InvManage', '0018_auto_20200409_1436'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchaseorder',
            name='balance',
            field=models.FloatField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='purchaseorder',
            name='date',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True),
        ),
        migrations.AlterField(
            model_name='purchaseorder',
            name='discount',
            field=models.FloatField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='purchaseorder',
            name='ordertotal',
            field=models.FloatField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='purchaseorder',
            name='paid',
            field=models.FloatField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='purchaseorder',
            name='subtotal',
            field=models.FloatField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='purchaseorder',
            name='tax',
            field=models.FloatField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='purchaseorder',
            name='taxtotal',
            field=models.FloatField(default=0, null=True),
        ),
    ]
