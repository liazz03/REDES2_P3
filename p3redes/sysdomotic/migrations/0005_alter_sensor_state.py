# Generated by Django 3.2.1 on 2023-05-03 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sysdomotic', '0004_alter_interruptor_state'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sensor',
            name='state',
            field=models.IntegerField(default=0),
        ),
    ]
