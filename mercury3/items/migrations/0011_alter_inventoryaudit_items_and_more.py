# Generated by Django 4.1.7 on 2023-03-17 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0010_inventoryaudit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventoryaudit',
            name='items',
            field=models.ManyToManyField(blank=True, null=True, related_name='all_inventory', to='items.item'),
        ),
        migrations.AlterField(
            model_name='inventoryaudit',
            name='items_left',
            field=models.ManyToManyField(blank=True, null=True, related_name='inventory_left', to='items.item'),
        ),
        migrations.AlterField(
            model_name='item',
            name='status',
            field=models.CharField(choices=[('pawn', 'Pawn'), ('redeem', 'Redeemed'), ('saleable', 'Saleable'), ('sold', 'Sold'), ('hold', 'Hold'), ('police_hold', 'Police Hold'), ('missing', 'Missing')], max_length=11),
        ),
    ]