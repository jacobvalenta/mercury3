# Generated by Django 4.2b1 on 2023-03-03 21:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0002_alter_item_make_alter_item_model'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='status',
            field=models.CharField(choices=[('sale', 'Sellable'), ('hold', 'Hold')], default='hold', max_length=10),
            preserve_default=False,
        ),
    ]
