# Generated by Django 3.2.1 on 2023-04-30 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sysdomotic', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Evento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('evento', models.CharField(max_length=100)),
            ],
        ),
    ]
