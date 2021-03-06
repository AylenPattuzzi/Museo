# Generated by Django 3.2.4 on 2021-07-30 18:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AsignacionVisita',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fechaHoraFin', models.DateTimeField()),
                ('fechaHoraInicio', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='CambioEstado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fechaHoraFin', models.DateTimeField()),
                ('fechaHoraInicio', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Cargo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.CharField(max_length=200)),
                ('nombre', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='DiaSemana',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Empleado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('apellido', models.CharField(max_length=15)),
                ('codigoValidacion', models.IntegerField()),
                ('cuit', models.BigIntegerField()),
                ('dni', models.IntegerField()),
                ('domicilio', models.CharField(max_length=50)),
                ('fechaIngreso', models.DateField()),
                ('fechaNacimiento', models.DateField()),
                ('mail', models.CharField(max_length=50)),
                ('nombre', models.CharField(max_length=15)),
                ('sexo', models.CharField(max_length=12)),
                ('telefono', models.BigIntegerField()),
                ('cargo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Visita.cargo')),
            ],
        ),
        migrations.CreateModel(
            name='Escuela',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('domicilio', models.CharField(max_length=50)),
                ('mail', models.CharField(max_length=50)),
                ('nombre', models.CharField(max_length=20)),
                ('telefCelular', models.IntegerField()),
                ('telfFijo', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Estado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ambito', models.CharField(max_length=15)),
                ('descripcion', models.CharField(max_length=50)),
                ('nombre', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Exposicion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fechaFinReplanificada', models.DateField()),
                ('fechaInicio', models.DateField()),
                ('fechaInicioReplanificada', models.DateField()),
                ('horaApertura', models.TimeField()),
                ('horaCierre', models.TimeField()),
                ('nombre', models.CharField(max_length=50)),
                ('empleado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Visita.empleado')),
            ],
        ),
        migrations.CreateModel(
            name='PublicoDestino',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caracteristicas', models.CharField(max_length=50)),
                ('nombre', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='TipoExposicion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.CharField(max_length=50)),
                ('nombre', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='TipoVisita',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caducidad', models.DateField()),
                ('contrasenia', models.CharField(max_length=20)),
                ('nombre', models.CharField(max_length=60)),
                ('empleado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Visita.empleado')),
            ],
        ),
        migrations.CreateModel(
            name='Tarifa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fechaFinVigencia', models.DateField()),
                ('fechaInicioVigencia', models.DateField()),
                ('monto', models.DecimalField(decimal_places=4, max_digits=13)),
                ('montoAdicionalGuia', models.DecimalField(decimal_places=4, max_digits=13)),
                ('tipoVisita', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Visita.tipovisita')),
            ],
        ),
        migrations.CreateModel(
            name='Sesion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fechaFin', models.DateField()),
                ('fechaInicio', models.DateField()),
                ('horaFin', models.TimeField()),
                ('horaInicio', models.TimeField()),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Visita.usuario')),
            ],
        ),
        migrations.CreateModel(
            name='Sede',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantMaximaVisitantes', models.IntegerField()),
                ('cantMaxPorGuia', models.IntegerField()),
                ('nombre', models.CharField(max_length=20)),
                ('exposicion', models.ManyToManyField(to='Visita.Exposicion')),
                ('tarifa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Visita.tarifa')),
            ],
        ),
        migrations.CreateModel(
            name='ReservaVisita',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidadAlumnos', models.IntegerField()),
                ('cantidadAlumnosConfirmada', models.IntegerField()),
                ('duracionExtendida', models.DurationField()),
                ('fechaHoraCreacion', models.DateTimeField()),
                ('fechaHoraReserva', models.DateTimeField()),
                ('horaFinReal', models.TimeField()),
                ('horaInicioReal', models.TimeField()),
                ('numeroReserva', models.IntegerField()),
                ('asignacionGuia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Visita.asignacionvisita')),
                ('cabioEstado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Visita.cambioestado')),
                ('empleado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Visita.empleado')),
                ('escuela', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Visita.escuela')),
                ('exposicion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Visita.exposicion')),
                ('sede', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Visita.sede')),
            ],
        ),
        migrations.CreateModel(
            name='Obra',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('alto', models.FloatField()),
                ('ancho', models.FloatField()),
                ('codigoSensor', models.IntegerField()),
                ('descripcion', models.CharField(max_length=50)),
                ('duracionExtendida', models.DurationField()),
                ('fechaCreacion', models.DateField()),
                ('fechaPrimerIngreso', models.DateField()),
                ('nombreObra', models.CharField(max_length=20)),
                ('peso', models.FloatField()),
                ('valuacion', models.FloatField()),
                ('cambioEstado', models.ManyToManyField(to='Visita.CambioEstado')),
                ('empleado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Visita.empleado')),
            ],
        ),
        migrations.CreateModel(
            name='HorarioEmpleado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('horaIngreso', models.TimeField()),
                ('horaSalida', models.TimeField()),
                ('diaSemana', models.ManyToManyField(to='Visita.DiaSemana')),
            ],
        ),
        migrations.AddField(
            model_name='exposicion',
            name='publicoDestino',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Visita.publicodestino'),
        ),
        migrations.AddField(
            model_name='exposicion',
            name='tipoExposicion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Visita.tipoexposicion'),
        ),
        migrations.AddField(
            model_name='empleado',
            name='horarioEmpleado',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Visita.horarioempleado'),
        ),
        migrations.AddField(
            model_name='empleado',
            name='sedeDondeTrabaja',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Visita.sede'),
        ),
        migrations.CreateModel(
            name='DetalleExposicion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lugarAsignado', models.CharField(max_length=50)),
                ('obra', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Visita.obra')),
            ],
        ),
        migrations.AddField(
            model_name='cambioestado',
            name='estado',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Visita.estado'),
        ),
        migrations.AddField(
            model_name='asignacionvisita',
            name='guiaAsignado',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Visita.empleado'),
        ),
    ]
