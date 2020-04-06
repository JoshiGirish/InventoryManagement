# Generated by Django 2.2.12 on 2020-04-04 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('InvManage', '0011_auto_20200404_1918'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='purchaseorder',
            name='products',
        ),
        migrations.AlterField(
            model_name='vendor',
            name='address',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='email',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='identifier',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='location',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='phone',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]