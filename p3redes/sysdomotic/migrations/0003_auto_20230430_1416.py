# Generated by Django 3.2.1 on 2023-04-30 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sysdomotic', '0002_evento'),
    ]

    operations = [
        migrations.AddField(
            model_name='interruptor',
            name='publicId',
            field=models.IntegerField(blank=True, default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='reloj',
            name='publicId',
            field=models.IntegerField(blank=True, default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sensor',
            name='publicId',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
