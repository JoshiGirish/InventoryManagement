# Generated by Django 2.2.12 on 2020-10-25 07:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('InvManage', '0063_auto_20201022_2242'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productpurchaseentry',
            name='status',
        ),
        migrations.RemoveField(
            model_name='purchaseorder',
            name='status',
        ),
        migrations.AlterField(
            model_name='purchaseorder',
            name='date',
            field=models.DateTimeField(blank=True, default='25 October, 2020', null=True),
        ),
    ]
