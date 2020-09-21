# Generated by Django 2.2.12 on 2020-09-20 13:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('InvManage', '0058_auto_20200803_2225'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Sale',
        ),
        migrations.AddField(
            model_name='purchaseinvoice',
            name='communication',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='InvManage.Communication'),
        ),
        migrations.AlterField(
            model_name='bankaccount',
            name='acctype',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Account Type'),
        ),
        migrations.AlterField(
            model_name='bankaccount',
            name='branchcode',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='Branch Code'),
        ),
        migrations.AlterField(
            model_name='bankaccount',
            name='code',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='Bank Code'),
        ),
        migrations.AlterField(
            model_name='bankaccount',
            name='iban',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='IBAN Number'),
        ),
        migrations.AlterField(
            model_name='bankaccount',
            name='name',
            field=models.CharField(max_length=100, null=True, verbose_name='Bank Name'),
        ),
        migrations.AlterField(
            model_name='bankaccount',
            name='number',
            field=models.IntegerField(null=True, verbose_name='Account Number'),
        ),
        migrations.AlterField(
            model_name='bankaccount',
            name='route',
            field=models.CharField(max_length=20, null=True, verbose_name='Transit Routing Number'),
        ),
        migrations.AlterField(
            model_name='purchasedata',
            name='contactperson',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Sales Person'),
        ),
        migrations.AlterField(
            model_name='purchasedata',
            name='currency',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='PO Currency'),
        ),
        migrations.AlterField(
            model_name='purchasedata',
            name='minorder',
            field=models.IntegerField(blank=True, null=True, verbose_name='Min Order Quantity'),
        ),
        migrations.AlterField(
            model_name='purchasedata',
            name='refcode',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Customer ID at Vendor'),
        ),
        migrations.AlterField(
            model_name='purchasedata',
            name='transportmode',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Transport Mode'),
        ),
        migrations.AlterField(
            model_name='shippingaddress',
            name='address',
            field=models.TextField(blank=True, null=True, verbose_name='Street'),
        ),
        migrations.AlterField(
            model_name='shippingaddress',
            name='post',
            field=models.CharField(max_length=20, null=True, verbose_name='Postal Code'),
        ),
    ]
