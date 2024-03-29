# Generated by Django 4.2rc1 on 2023-03-23 17:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('drawers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DrawerIdentifier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=14)),
            ],
        ),
        migrations.RemoveField(
            model_name='drawer',
            name='number',
        ),
        migrations.AddField(
            model_name='drawer',
            name='identifier_key',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='drawers.draweridentifier'),
        ),
    ]
