# Generated by Django 2.2.12 on 2021-02-22 20:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('InvManage', '0071_auto_20210221_2304'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchaseorder',
            name='date',
            field=models.DateTimeField(blank=True, default='22 February, 2021', null=True),
        ),
    ]
