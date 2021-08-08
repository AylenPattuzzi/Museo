# Generated by Django 3.2.4 on 2021-08-08 18:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Visita', '0010_auto_20210808_1418'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservavisita',
            name='empleado',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Visita.empleado'),
        ),
        migrations.AlterField(
            model_name='reservavisita',
            name='escuela',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Visita.escuela'),
        ),
        migrations.AlterField(
            model_name='reservavisita',
            name='sede',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Visita.sede'),
        ),
    ]