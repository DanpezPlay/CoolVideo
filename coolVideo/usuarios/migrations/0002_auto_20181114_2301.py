# Generated by Django 2.1.3 on 2018-11-15 05:01

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publicacion',
            name='creado',
            field=models.DateTimeField(default=datetime.datetime(2018, 11, 15, 5, 1, 1, 498871, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='publicacion',
            name='editado',
            field=models.DateTimeField(default=datetime.datetime(2018, 11, 15, 5, 1, 1, 498898, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='creado',
            field=models.DateTimeField(default=datetime.datetime(2018, 11, 15, 5, 1, 1, 498263, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='editado',
            field=models.DateTimeField(default=datetime.datetime(2018, 11, 15, 5, 1, 1, 498299, tzinfo=utc)),
        ),
    ]
