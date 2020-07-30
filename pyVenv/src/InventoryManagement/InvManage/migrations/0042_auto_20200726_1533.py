# Generated by Django 2.2.12 on 2020-07-26 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('InvManage', '0041_auto_20200725_2042'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='eventtype',
            name='created',
        ),
        migrations.RemoveField(
            model_name='eventtype',
            name='deleted',
        ),
        migrations.RemoveField(
            model_name='eventtype',
            name='state',
        ),
        migrations.RemoveField(
            model_name='eventtype',
            name='updated',
        ),
        migrations.RemoveField(
            model_name='objectmodel',
            name='company',
        ),
        migrations.RemoveField(
            model_name='objectmodel',
            name='consumer',
        ),
        migrations.RemoveField(
            model_name='objectmodel',
            name='po',
        ),
        migrations.RemoveField(
            model_name='objectmodel',
            name='product',
        ),
        migrations.RemoveField(
            model_name='objectmodel',
            name='so',
        ),
        migrations.RemoveField(
            model_name='objectmodel',
            name='state',
        ),
        migrations.RemoveField(
            model_name='objectmodel',
            name='vendor',
        ),
        migrations.AddField(
            model_name='eventtype',
            name='name',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='historyfilterstate',
            name='events',
            field=models.ManyToManyField(to='InvManage.EventType'),
        ),
        migrations.AddField(
            model_name='historyfilterstate',
            name='mods',
            field=models.ManyToManyField(to='InvManage.ObjectModel'),
        ),
        migrations.AddField(
            model_name='objectmodel',
            name='name',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
