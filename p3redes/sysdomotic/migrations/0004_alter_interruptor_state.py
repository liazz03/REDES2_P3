# Generated by Django 3.2.1 on 2023-05-02 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sysdomotic', '0003_auto_20230430_1416'),
    ]

    operations = [
        migrations.AlterField(
            model_name='interruptor',
            name='state',
            field=models.CharField(default='OFF', max_length=50),
        ),
    ]
