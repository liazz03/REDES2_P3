# Generated by Django 3.2.1 on 2023-05-06 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sysdomotic', '0006_auto_20230505_0856'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reloj',
            name='state',
            field=models.CharField(default='00:00:00', max_length=8),
        ),
    ]
