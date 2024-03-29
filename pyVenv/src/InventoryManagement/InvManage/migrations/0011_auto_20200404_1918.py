# Generated by Django 2.2.12 on 2020-04-04 13:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('InvManage', '0010_auto_20200325_1958'),
    ]

    operations = [
        migrations.CreateModel(
            name='PurchaseOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(blank=True, null=True)),
                ('po', models.IntegerField()),
                ('discount', models.IntegerField()),
                ('tax', models.FloatField()),
                ('paid', models.FloatField()),
                ('balance', models.FloatField()),
                ('products', models.ManyToManyField(to='InvManage.Product')),
            ],
        ),
        migrations.CreateModel(
            name='Vendor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('identifier', models.CharField(max_length=100)),
                ('phone', models.IntegerField()),
                ('address', models.TextField()),
                ('email', models.CharField(max_length=100)),
                ('location', models.CharField(max_length=100)),
            ],
        ),
        migrations.DeleteModel(
            name='Purchase',
        ),
        migrations.AddField(
            model_name='purchaseorder',
            name='vendor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='InvManage.Vendor'),
        ),
    ]
