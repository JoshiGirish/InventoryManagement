# Generated by Django 2.2.12 on 2020-10-02 18:27

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('InvManage', '0059_auto_20200920_1914'),
    ]

    operations = [
        migrations.CreateModel(
            name='GoodsReceiptNote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.IntegerField()),
                ('date', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('grnType', models.CharField(choices=[('manual', 'Blank'), ('auto', 'PO Reference')], default='manual', max_length=10, null=True)),
                ('amendNumber', models.IntegerField(blank=True, default=0, null=True)),
                ('amendDate', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('vehicleNumber', models.TextField(blank=True, default=None, null=True)),
                ('gateInwardNumber', models.TextField(blank=True, default=None, null=True)),
                ('preparedBy', models.CharField(blank=True, default=None, max_length=50, null=True)),
                ('checkedBy', models.CharField(blank=True, default=None, max_length=50, null=True)),
                ('inspectedBy', models.CharField(blank=True, default=None, max_length=50, null=True)),
                ('approvedBy', models.CharField(blank=True, default=None, max_length=50, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='productpurchaseentry',
            name='acceptedQty',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='productpurchaseentry',
            name='receivedQty',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='productpurchaseentry',
            name='rejectedQty',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='productpurchaseentry',
            name='status',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AddField(
            model_name='purchaseorder',
            name='status',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.CreateModel(
            name='GRNEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(null=True)),
                ('remark', models.TextField(blank=True, default=None, null=True)),
                ('receivedQty', models.IntegerField(blank=True, default=0, null=True)),
                ('acceptedQty', models.IntegerField(blank=True, default=0, null=True)),
                ('rejectedQty', models.IntegerField(blank=True, default=0, null=True)),
                ('grn', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='InvManage.GoodsReceiptNote')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='InvManage.Product')),
            ],
        ),
        migrations.AddField(
            model_name='goodsreceiptnote',
            name='poRef',
            field=models.ManyToManyField(to='InvManage.PurchaseOrder'),
        ),
        migrations.AddField(
            model_name='goodsreceiptnote',
            name='vendor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='InvManage.Vendor'),
        ),
    ]