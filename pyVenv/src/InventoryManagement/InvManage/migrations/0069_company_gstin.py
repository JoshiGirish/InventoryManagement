# Generated by Django 2.2.12 on 2021-02-20 05:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('InvManage', '0068_auto_20210220_1127'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='gstin',
            field=models.CharField(default=None, max_length=100, null=True),
        ),
    ]