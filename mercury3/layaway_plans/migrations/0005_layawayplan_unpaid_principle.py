# Generated by Django 4.1.7 on 2023-03-14 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('layaway_plans', '0004_layawayplan_items'),
    ]

    operations = [
        migrations.AddField(
            model_name='layawayplan',
            name='unpaid_principle',
            field=models.DecimalField(decimal_places=2, default=1.0, max_digits=9),
            preserve_default=False,
        ),
    ]
