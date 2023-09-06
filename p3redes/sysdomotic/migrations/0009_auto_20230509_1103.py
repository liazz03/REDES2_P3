# Generated by Django 3.2.1 on 2023-05-09 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sysdomotic', '0008_remove_reloj_state'),
    ]

    operations = [
        migrations.AlterField(
            model_name='interruptor',
            name='publicId',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='regla',
            name='regla',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='reloj',
            name='publicId',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='sensor',
            name='publicId',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
