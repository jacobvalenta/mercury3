# Generated by Django 4.1.7 on 2023-03-12 01:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('layaway_plans', '0002_layawayplan_date_due'),
    ]

    operations = [
        migrations.AddField(
            model_name='layawayplan',
            name='status',
            field=models.CharField(choices=[('active', 'Active'), ('redeemed', 'Redeemed'), ('forfeited', 'Forfeited')], default='active', max_length=10),
            preserve_default=False,
        ),
    ]
