# Generated by Django 2.2.12 on 2020-07-26 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('InvManage', '0044_auto_20200726_2133'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventtype',
            name='name',
            field=models.CharField(default='old', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='objectmodel',
            name='name',
            field=models.CharField(default='old', max_length=100),
            preserve_default=False,
        ),
    ]
