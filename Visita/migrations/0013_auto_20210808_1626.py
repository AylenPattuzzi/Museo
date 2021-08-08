# Generated by Django 3.2.4 on 2021-08-08 19:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Visita', '0012_auto_20210808_1532'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asignacionvisita',
            name='fechaHoraFin',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='asignacionvisita',
            name='fechaHoraInicio',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='asignacionvisita',
            name='guiaAsignado',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Visita.empleado'),
        ),
    ]
