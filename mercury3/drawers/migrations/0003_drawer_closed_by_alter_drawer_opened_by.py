# Generated by Django 4.2rc1 on 2023-03-23 18:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0006_employee_changed_at_historicalemployee_changed_at'),
        ('drawers', '0002_draweridentifier_remove_drawer_number_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='drawer',
            name='closed_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='closing_employee', to='employees.employee'),
        ),
        migrations.AlterField(
            model_name='drawer',
            name='opened_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='opening_employee', to='employees.employee'),
        ),
    ]