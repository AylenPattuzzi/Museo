# Generated by Django 3.2.4 on 2021-08-07 04:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Visita', '0008_auto_20210807_0144'),
    ]

    operations = [
        migrations.AlterField(
            model_name='escuela',
            name='telefCelular',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='escuela',
            name='telfFijo',
            field=models.BigIntegerField(blank=True, null=True),
        ),
    ]
