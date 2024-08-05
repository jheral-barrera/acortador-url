# Generated by Django 5.0.1 on 2024-01-16 02:02

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('enlaces', '0003_alter_enlace_id_alter_enlace_url_acortado'),
    ]

    operations = [
        migrations.AddField(
            model_name='enlace',
            name='clics_totales',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='enlace',
            name='fecha_creacion',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 16, 2, 2, 1, 521441, tzinfo=datetime.timezone.utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='enlace',
            name='fecha_ultimo_clic',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='enlace',
            name='url_acortado',
            field=models.CharField(blank=True, max_length=8, unique=True),
        ),
    ]