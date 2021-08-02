from django.db import models
import datetime

class DiaSemana(models.Model):
    nombre = models.CharField(max_length=20)
    def getNombre(self):
        return self.nombre

class HorarioEmpleado(models.Model):
    horaIngreso = models.TimeField()
    horaSalida = models.TimeField()
    diaSemana = models.ManyToManyField(DiaSemana)
    #def obtenerJornadaLaboral(self):
        #ToDo
     #   return None
    def trabajaEnHorario(self, dia, horarioInicio, horarioFin):
        esMiDia = False
        for dia in DiaSemana:
            if dia.getNombre().lower() == dia:
                esMiDia = True
                break
        if not esMiDia:
            return False #no es mi dia
        if self.horaIngreso <= horarioInicio and self.horaSalida > horarioFin:
            return True # es mi dia y horario
        else:
            return False #es mi dia pero no mi horario

    def getHoraFin(self):
        return self.horaSalida
    def getHoraInicio(self):
        return self.horaIngreso

class Escuela(models.Model):
    domicilio = models.CharField(max_length=50, blank=True, null=True)
    mail = models.CharField(max_length=50, blank=True, null=True)
    nombre = models.CharField(max_length=20)
    telefCelular = models.IntegerField(blank=True, null=True)
    telfFijo = models.IntegerField(blank=True, null=True)
    def getNombre(self):
        return self.nombre

class AsignacionVisita(models.Model):
    fechaHoraFin = models.DateTimeField()
    fechaHoraInicio = models.DateTimeField()
    guiaAsignado = models.ForeignKey("Empleado", on_delete=models.CASCADE) 
    #def tieneAsignadoVisitas(self):
    def esAsignadoEnHorario(self, horarioInicio, horarioFin):
        if self.fechaHoraInicio <= horarioInicio and self.fechaHoraFin > horarioInicio:
            return True
        elif self.fechaHoraInicio < horarioFin and self.fechaHoraFin >= horarioFin:
            return True
        else:
            return False

class TipoExposicion(models.Model):
    descripcion = models.CharField(max_length=50, blank=True, null=True)
    nombre = models.CharField(max_length=20)
    def esTemporal(self):
        if self.nombre.lower() == "temporal":
            return True
        else:
            return False
        

class PublicoDestino(models.Model):
    caracteristicas = models.CharField(max_length=50, blank=True, null=True)
    nombre  = models.CharField(max_length=20)
    def mostrarNombre(self):
        return self.nombre

class CambioEstado(models.Model):
    fechaHoraFin = models.DateTimeField() 
    fechaHoraInicio = models.DateTimeField()
    estado = models.ForeignKey("Estado", on_delete=models.CASCADE)
    def setEstado(self, estado):
        self.estado = estado

class Estado(models.Model):
    ambito = models.CharField(max_length=15)
    descripcion = models.CharField(max_length=50, blank=True, null=True)
    nombre = models.CharField(max_length=20)
    def esPendienteDeConfirmacion(self):
        if self.nombre.lower() == "pendiente de confirmación":
            return True
        else:
            return False

class Obra(models.Model):
    alto = models.FloatField(blank=True, null=True)
    ancho = models.FloatField(blank=True, null=True)
    codigoSensor = models.IntegerField(blank=True, null=True)
    descripcion = models.CharField(max_length=50, blank=True, null=True)
    duracionExtendida = models.DurationField()
    duracionResumida = models.DurationField() 
    fechaCreacion = models.DateField()
    fechaPrimerIngreso = models.DateField(blank=True, null=True)
    nombreObra = models.CharField(max_length=20)
    peso = models.FloatField(blank=True, null=True)
    valuacion = models.FloatField(blank=True, null=True) 
    cambioEstado = models.ManyToManyField(CambioEstado, blank=True) ## ---------------
    empleado = models.ForeignKey("Empleado", on_delete=models.CASCADE, blank=True) #----------
    def getDuracionExtendida(self):
        return self.duracionExtendida
    def getDuracionResumida(self):
        return self.duracionResumida


class DetalleExposicion(models.Model):
    lugarAsignado = models.CharField(max_length=50, blank=True, null=True)
    obra = models.ForeignKey(Obra, on_delete=models.CASCADE)
    def buscarDuracExtObra(self):
        return self.obra.getDuracionExtendida()
    def buscarDuracResObra(self):
        return self.obra.getDuracionResumida()

class Usuario(models.Model):
    caducidad = models.DateField(blank=True, null=True)
    contrasenia = models.CharField(max_length=20)
    nombre = models.CharField(max_length=60)
    empleado = models.ForeignKey("Empleado", on_delete=models.CASCADE)
    def getResponsable(self):
        return self.empleado.getNombre()

class Sesion(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fechaFin = models.DateField(blank=True, null=True)
    fechaInicio = models.DateField(blank=True, null=True)
    horaFin = models.TimeField()
    horaInicio = models.TimeField()
    def mostrarResponsable(self):
        return self.usuario.getResponsable()

class Cargo(models.Model):
    descripcion = models.CharField(max_length= 200, blank=True, null=True)
    nombre = models.CharField(max_length= 40)
    def esGuia(self):
        if self.nombre.lower() == "guía":
            return True
        else:
            return False

class Exposicion(models.Model):
    fechaFin = models.DateField(blank=True, null=True)
    fechaFinReplanificada = models.DateField(blank=True, null=True)
    fechaInicio = models.DateField()
    fechaInicioReplanificada = models.DateField(blank=True, null=True)
    horaApertura = models.TimeField()
    horaCierre = models.TimeField()
    nombre = models.CharField(max_length= 50)
    empleado=models.ForeignKey("Empleado", on_delete=models.CASCADE)
    tipoExposicion = models.ForeignKey(TipoExposicion, on_delete=models.CASCADE, blank=True, null=True)
    publicoDestino = models.ForeignKey(PublicoDestino, on_delete=models.CASCADE, blank=True, null=True)
    detalleExposicion = models.ManyToManyField(DetalleExposicion, blank=True)
    def esTemporal(self):
        return self.tipoExposicion.esTemporal()
    def esVigente(self, fechaActual):
        if self.fechaInicio <= fechaActual and self.fechaFin >= fechaActual:
            return True 
        else:
            return False

    def obtenerPublicoDestino(self):
        return self.publicoDestino.mostarNombre()

    def getHoraApertura(self):
        return self.horaApertura

    def getHoraCierre(self):
        return self.horaCierre

    def calcularDuracionObrasExpuestas(self, tipoVisitaSeleccionada):
        duracion = datetime.timedelta(0)
        for detalleExposicion in self.detalleExposicion.all():
            if tipoVisitaSeleccionada.lower() == "por exposición": # Observación 2, si es por exposición se suman las duraciónes extendidas, si es completa las resumidas
                # flujo básico, duración extendida
                duracion += detalleExposicion.buscarDuracExtObra()
            else:
                # flujo alternativo, tipo de visita = completo, duracion resumida
                duracion += detalleExposicion.buscarDuracResObra()
        return duracion

    def buscarGuiasDisponibles(self, dia, horarioInicio, horarioFin):
        return self.empleado.tieneAsignacionesEnHorario(dia, horarioInicio, horarioFin)

class TipoVisita(models.Model):
    nombre = models.CharField(max_length=20)
    def mostrarNombre(self):
        return self.nombre

class Tarifa(models.Model):
    fechaFinVigencia = models.DateField(blank=True, null=True)
    fechaInicioVigencia = models.DateField()
    monto = models.DecimalField(decimal_places=4, max_digits=13)
    montoAdicionalGuia = models.DecimalField(decimal_places=4, max_digits=13)
    tipoVisita = models.ForeignKey(TipoVisita, on_delete=models.CASCADE) #------------
    def obtenerTipoVisita(self):
        return self.tipoVisita.mostrarNombre()

class Sede(models.Model):
    cantMaximaVisitantes = models.IntegerField()
    cantMaxPorGuia = models.IntegerField()
    nombre = models.CharField(max_length= 20)
    exposicion = models.ManyToManyField(Exposicion)
    tarifa = models.ManyToManyField(Tarifa) #------------------
    def getNombre(self):
        return self.nombre
    def obtenerExpTempVigente(self):
        #TODO ------------------------------------------
        nombres = []
        for expo in Exposicion.objects.all():
            nombres.append(expo.nombre)
        return nombres
    def calcularDuracionDeExposicionesSeleccionadas(self, tipoVisitaSeleccionada, exposicionSeleccionada):
        duracion = datetime.timedelta(0)
        for exposicion in exposicionSeleccionada:
            duracion += exposicion.calcularDuracionObrasExpuestas(tipoVisitaSeleccionada)
        return duracion
    def getCantMaximaVisitantes(self):
        return self.cantMaximaVisitantes 
    def buscarGuiasDisponibles(self, dia, horarioInicio, horarioFin):
        return self.exposicion.buscarGuiasDisponibles(dia, horarioInicio, horarioFin)
    def getCantMaxPorGuia(self):
        return self.cantMaxPorGuia

class Empleado(models.Model):
    apellido = models.CharField(max_length= 15)
    codigoValidacion = models.IntegerField(blank=True, null=True)
    cuit = models.BigIntegerField(blank=True, null=True)
    dni = models.IntegerField(blank=True, null=True)
    domicilio = models.CharField(max_length= 50, blank=True, null=True)
    fechaIngreso = models.DateField(blank=True, null=True)
    fechaNacimiento = models.DateField(blank=True, null=True)
    mail =  models.CharField(max_length= 50, blank=True, null=True)
    nombre = models.CharField(max_length= 15)
    sexo = models.CharField(max_length= 12, blank=True, null=True)
    telefono = models.BigIntegerField(blank=True, null=True)
    cargo = models.ForeignKey(Cargo, on_delete=models.CASCADE, blank=True, null=True)
    horarioEmpleado = models.ManyToManyField(HorarioEmpleado, blank=True)
    sedeDondeTrabaja = models.ForeignKey(Sede, on_delete=models.CASCADE, blank=True, null=True)
    def getNombre(self):
        return self.nombre
    def tieneAsignacionesEnHorario(self, dia, horarioInicio, horarioFin):
        
        if not self.cargo.esGuia():
           return None # significa que no es un guia
        
        trabajaEnHorario = False # bandera

        for horario in self.horarioEmpleado.all(): #loop horarios empleado
            
            #horario.obtenerJornadaLaboral() rompe el patron "lo hace quien conoce"
            
            if horario.trabajaEnHorario(dia, horarioInicio, horarioFin): #dejo que "quien conoce" haga el cálculo
                trabajaEnHorario = True 
                break
        
        if not trabajaEnHorario:
            return None # significa que no trabaja en ese horario
        
        for asignacion in AsignacionVisita.objects.all():
            if asignacion.guiaAsignado == self:
                if asignacion.esAsignadoEnHorario(horarioInicio, horarioFin): #respeta el patron "lo hace quien conoce"
                    return True # significa que ya está asignado

        return False #significa que no fue asignado, pero si trabaja en el horario solicitado.

class ReservaVisita(models.Model):
    cantidadAlumnos = models.IntegerField(blank=True, null=True)
    cantidadAlumnosConfirmada = models. IntegerField(blank=True, null=True)
    duracionExtendida = models. DurationField(blank=True, null=True)
    fechaHoraCreacion = models.DateTimeField(blank=True, null=True)
    fechaHoraReserva = models.DateTimeField(blank=True, null=True)
    horaFinReal = models.TimeField(blank=True, null=True)
    horaInicioReal = models.TimeField(blank=True, null=True)
    numeroReserva = models.IntegerField(blank=True, null=True)
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    asignacionGuia = models.ForeignKey(AsignacionVisita, on_delete=models.CASCADE)
    escuela = models.ForeignKey(Escuela, on_delete=models.CASCADE)
    sede = models.ForeignKey(Sede, on_delete=models.CASCADE)
    exposicion = models.ForeignKey(Exposicion, on_delete=models.CASCADE)
    cabioEstado = models.ForeignKey(CambioEstado, on_delete=models.CASCADE)
    def getCantAlumnos(self):
        return self.cantidadAlumnos
    def getCantMaximaVisitantes(self):
        return self.sede.getCantMaximaVisitantes()
    def getNumeroReserva(self):
        return self.numeroReserva
    def crearCambioEstado(self):
        #ToDo
        return