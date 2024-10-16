# Generated by Django 5.1.2 on 2024-10-13 06:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_domain'),
    ]

    operations = [
        migrations.AlterField(
            model_name='domain',
            name='domain',
            field=models.CharField(max_length=253),
        ),
        migrations.AlterField(
            model_name='domain',
            name='is_primary',
            field=models.BooleanField(default=False),
        ),
    ]
