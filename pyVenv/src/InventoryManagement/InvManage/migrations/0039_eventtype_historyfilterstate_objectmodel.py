# Generated by Django 2.2.12 on 2020-07-25 14:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('InvManage', '0038_eventcard_objid'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoryFilterState',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('numEntries', models.IntegerField(default=10)),
            ],
        ),
        migrations.CreateModel(
            name='ObjectModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company', models.BooleanField(default=True)),
                ('vendor', models.BooleanField(default=True)),
                ('po', models.BooleanField(default=True)),
                ('product', models.BooleanField(default=True)),
                ('consumer', models.BooleanField(default=True)),
                ('so', models.BooleanField(default=True)),
                ('state', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='InvManage.HistoryFilterState')),
            ],
        ),
        migrations.CreateModel(
            name='EventType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.BooleanField(default=True)),
                ('updated', models.BooleanField(default=True)),
                ('deleted', models.BooleanField(default=True)),
                ('state', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='InvManage.HistoryFilterState')),
            ],
        ),
    ]