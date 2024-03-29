# Generated by Django 2.2.12 on 2021-02-07 05:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('InvManage', '0064_auto_20201025_1247'),
    ]

    operations = [
        migrations.AddField(
            model_name='goodsreceiptnote',
            name='transporter',
            field=models.TextField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='goodsreceiptnote',
            name='vehicleNumber',
            field=models.TextField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='purchaseorder',
            name='date',
            field=models.DateTimeField(blank=True, default='07 February, 2021', null=True),
        ),
        migrations.CreateModel(
            name='GRNInvoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='InvManage.Company')),
                ('grn', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='InvManage.GoodsReceiptNote')),
            ],
        ),
    ]
