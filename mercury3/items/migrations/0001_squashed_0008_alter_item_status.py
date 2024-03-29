# Generated by Django 4.1.7 on 2023-03-16 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    # replaces = [('items', '0001_initial'), ('items', '0002_alter_item_make_alter_item_model'), ('items', '0003_item_status'), ('items', '0004_item_price_item_price_in_item_price_out'), ('items', '0005_alter_item_status'), ('items', '0006_alter_item_price'), ('items', '0007_alter_item_status'), ('items', '0008_alter_item_status')]

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('make', models.CharField(blank=True, max_length=48, null=True)),
                ('model', models.CharField(blank=True, max_length=48, null=True)),
                ('status', models.CharField(choices=[('pawn', 'Pawn'), ('redeem', 'Redeemed'), ('saleable', 'Saleable'), ('sold', 'Sold'), ('hold', 'Hold'), ('police_hold', 'Police Hold')], max_length=11)),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=9, null=True)),
                ('price_in', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('price_out', models.DecimalField(blank=True, decimal_places=2, max_digits=9, null=True)),
            ],
        ),
    ]
