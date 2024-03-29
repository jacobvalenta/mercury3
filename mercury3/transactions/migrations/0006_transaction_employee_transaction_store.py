# Generated by Django 4.1.7 on 2023-03-19 00:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stores', '0001_initial'),
        ('employees', '0002_remove_employee_first_name_remove_employee_last_name'),
        ('transactions', '0005_alter_transaction_transaction_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='employee',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='employees.employee'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='transaction',
            name='store',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='stores.store'),
            preserve_default=False,
        ),
    ]
