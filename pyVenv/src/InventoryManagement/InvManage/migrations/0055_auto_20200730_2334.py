# Generated by Django 2.2.12 on 2020-07-30 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('InvManage', '0054_auto_20200730_2326'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventcard',
            name='date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
