from django.core import serializers
from django.db import models
import datetime

#!Este es el formato de la clase aplicado para todo, hereda el Model que es el ORM de django
#!Se definen los atributos y un tipo de campo para ese atributo, charField para caracteres varios, timeFieldtemporales y Many to Many cuando es una relacion
#!de muchos a muchos entre clases
class DiaSemana(models.Model):
    nombre = models.CharField(max_length=20)

    #!Asi se define los metodos de las clases, en este caso es un get sobre el nombre 
    def getNombre(self):
        return self.nombre

class HorarioEmpleado(models.Model):
    horaIngreso = models.TimeField()
    horaSalida = models.TimeField()
    diaSemana = models.ManyToManyField(DiaSemana)
    
    def trabajaEnHorario(self, dia, horarioInicio, horarioFin):
        esMiDia = False #booleano que indica si ese horario aplica ese dia
        for diaSemana in self.diaSemana.all():
            if diaSemana.getNombre().lower() == dia:
                esMiDia = True #Si el dia de la semana es el dia del horario, si aplica ese dia
                break
        if not esMiDia:
            return False #no es mi dia
        if self.getHoraIngreso() <= horarioInicio and self.getHoraSalida() > horarioFin:
            return True # es mi dia y horario
        else:
            return False #es mi dia pero no mi horario

    def getHoraSalida(self):
        return self.horaSalida
    def getHoraIngreso(self):
        return self.horaIngreso

class Escuela(models.Model):
    domicilio = models.CharField(max_length=50, blank=True, null=True) #Tambien se muestra el maximo de caracteres, si puede estar vacio o ser null
    mail = models.CharField(max_length=50, blank=True, null=True)
    nombre = models.CharField(max_length=100)
    telefCelular = models.BigIntegerField(blank=True, null=True)
    telfFijo = models.BigIntegerField(blank=True, null=True)
    def getNombre(self):
        return self.nombre

class AsignacionVisita(models.Model):
    fechaHoraFin = models.DateTimeField(blank=True, null=True)
    fechaHoraInicio = models.DateTimeField(blank=True, null=True)
    guiaAsignado = models.ForeignKey("Empleado", on_delete=models.CASCADE, blank=True, null=True) 
   
   
    def esAsignadoEnHorario(self, empleado, horarioInicio, horarioFin):
        if not self.guiaAsignado == empleado: #Si el guia de la asignacion actual es el empleado por el que preguntamos
            return False
        #Comprueba que el empleado parametro no tenga asignaciones en los horarios parametro comparando los horarios de la asignacion actual con el dato ingresado
        if self.fechaHoraInicio.replace(tzinfo=None) <= horarioInicio and self.fechaHoraFin.replace(tzinfo=None) > horarioInicio:
            return True
        elif self.fechaHoraInicio.replace(tzinfo=None) < horarioFin and self.fechaHoraFin.replace(tzinfo=None) >= horarioFin:
            return True
        else:
            return False
    #!Se crea una nueva asignacion y se asignan los valores de los atributos. De esta forma se realiza en todas las clases
    def new(self, empleado, fechaHoraInicio, fechaHoraFin):
        self.guiaAsignado = empleado
        self.fechaHoraInicio = fechaHoraInicio
        self.fechaHoraFin = fechaHoraFin

#Clase tipoExposicion
class TipoExposicion(models.Model):
    descripcion = models.CharField(max_length=50, blank=True, null=True)
    nombre = models.CharField(max_length=20)
    
    #Confirma si el tipo de exposicion es temporal
    def esTemporal(self):
        if self.nombre.lower() == "temporal": #Si es temporal devuelve valor booleano
            return True
        else:
            return False
        

class PublicoDestino(models.Model):
    caracteristicas = models.CharField(max_length=50, blank=True, null=True)
    nombre  = models.CharField(max_length=20)
    def mostrarNombre(self):
        return self.nombre

class CambioEstado(models.Model):
    fechaHoraFin = models.DateTimeField(blank=True, null=True) 
    fechaHoraInicio = models.DateTimeField(blank=True, null=True)
    estado = models.ForeignKey("Estado", on_delete=models.CASCADE, blank=True, null=True)
    def setEstado(self, estado):
        self.estado = estado
    def new(self, estado, fechaHoraActual):
        self.fechaHoraInicio = fechaHoraActual
        self.setEstado(estado)
        

class Estado(models.Model):
    ambito = models.CharField(max_length=15)
    descripcion = models.CharField(max_length=50, blank=True, null=True)
    nombre = models.CharField(max_length=50)

    #Si el estado es pendiente de confirmacion devuelve un boolean
    def esPendienteDeConfirmacion(self):
        if self.nombre.lower() == "pendientedeconfirmacion":
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
    nombreObra = models.CharField(max_length=50)
    peso = models.FloatField(blank=True, null=True)
    valuacion = models.FloatField(blank=True, null=True) 
    cambioEstado = models.ManyToManyField(CambioEstado, blank=True)
    empleado = models.ForeignKey("Empleado", on_delete=models.CASCADE, blank=True) 

    #Devuelven los atributos de duracion de la obra
    def getDuracionExtendida(self):
        return self.duracionExtendida
    def getDuracionResumida(self):
        return self.duracionResumida


class DetalleExposicion(models.Model):
    lugarAsignado = models.CharField(max_length=50, blank=True, null=True)
    obra = models.ForeignKey(Obra, on_delete=models.CASCADE)

    #llaman a los metodos de la obra para obtener las duraciones
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
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE) #!Asi se definen las Foreign Keys en relaciones de uno a muchos
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
        if self.nombre.lower() == "guia de exposicion":
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
    
    #Pregunta si el tipo de exposicion de una exposicion particular es temporal, llamando al metodo esTemporal de la clase TipoExposicion
    def esTemporal(self):
        return self.tipoExposicion.esTemporal()

    #Compara la fecha de inicio y de fin de una exposicion con la fecha actual (pasada como parametro)
    def esVigente(self, fechaActual):
        if self.fechaInicio <= fechaActual and self.fechaFin >= fechaActual:
            return True 
        else:
            return False

    #Obtiene el nombre del publicoDestino de la exposicion
    def obtenerPublicoDestino(self):
        return self.publicoDestino.mostarNombre()

    def getHoraApertura(self):
        return self.horaApertura

    def getHoraCierre(self):
        return self.horaCierre

    #Realiza una sumatoria de los tiempos de las obras de las exposiciones dependiendo el tipo de visita seleccionada
    def calcularDuracionObrasExpuestasPorExpo(self):
        duracion = datetime.timedelta(0)
        for detalleExposicion in self.detalleExposicion.all():
                # flujo basico, tipo de visita = por expo, duracion completa
                duracion += detalleExposicion.buscarDuracExtObra()
        return duracion
    
    def calcularDuracionObrasExpuestasCompleta(self):
        duracion = datetime.timedelta(0)
        for detalleExposicion in self.detalleExposicion.all():
                # flujo alternativo, tipo de visita = completo, duracion resumida
                duracion += detalleExposicion.buscarDuracResObra()
        return duracion
    

class TipoVisita(models.Model):
    nombre = models.CharField(max_length=20)
    def mostrarNombre(self):
        return self.nombre

class Tarifa(models.Model):
    fechaFinVigencia = models.DateField(blank=True, null=True)
    fechaInicioVigencia = models.DateField()
    monto = models.DecimalField(decimal_places=4, max_digits=13)
    montoAdicionalGuia = models.DecimalField(decimal_places=4, max_digits=13)
    tipoVisita = models.ForeignKey(TipoVisita, on_delete=models.CASCADE) 
    def obtenerTipoVisita(self):
        return self.tipoVisita.mostrarNombre()


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
    sedeDondeTrabaja = models.ForeignKey("Sede", on_delete=models.CASCADE, blank=True, null=True)
    def getNombre(self):
        return self.apellido + ", " + self.nombre

    
    def tieneAsignacionesEnHorario(self, dia, fechaHoraInicio, fechaHoraFin):
        if not self.cargo.esGuia():
            return None # significa que no es un guia
        
        trabajaEnHorario = False # bandera

        for horario in self.horarioEmpleado.all(): #loop horarios empleado
            
            #horario.obtenerJornadaLaboral() rompe el patron "lo hace quien conoce"
            if horario.trabajaEnHorario(dia, fechaHoraInicio.time(), fechaHoraFin.time()): #dejo que "quien conoce" haga el cálculo
                trabajaEnHorario = True 
        
        if not trabajaEnHorario:
            return None # significa que no trabaja en ese horario
        
        for asignacion in AsignacionVisita.objects.all():
            
            if asignacion.esAsignadoEnHorario(self, fechaHoraInicio, fechaHoraFin): #respeta el patron "lo hace quien conoce"
                return True # significa que ya está asignado (ocupado)

        return False #significa que no fue asignado, pero si trabaja en el horario solicitado. (libre)

class ReservaVisita(models.Model):
    cantidadAlumnos = models.IntegerField(blank=True, null=True)
    cantidadAlumnosConfirmada = models. IntegerField(blank=True, null=True)
    duracionEstimada = models. DurationField(blank=True, null=True)
    fechaHoraCreacion = models.DateTimeField(blank=True, null=True)
    fechaHoraReserva = models.DateTimeField(blank=True, null=True)
    horaFinReal = models.TimeField(blank=True, null=True)
    horaInicioReal = models.TimeField(blank=True, null=True)
    numeroReserva = models.IntegerField(blank=True, null=True)
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE, blank=True, null=True)
    asignacionGuia = models.ManyToManyField(AsignacionVisita)
    escuela = models.ForeignKey(Escuela, on_delete=models.CASCADE, blank=True, null=True)
    sede = models.ForeignKey("Sede", on_delete=models.CASCADE, blank=True, null=True)
    exposicion = models.ManyToManyField(Exposicion)
    cabioEstado = models.ManyToManyField(CambioEstado)
    def getCantVisitantes(self):
        return self.cantidadAlumnos
    def getCantMaximaVisitantes(self):
        return self.sede.getCantMaximaVisitantes()
        
    def getNumeroReserva(self):
        return self.numeroReserva
    
    #Recorre todos los cambios de estado de una reserva y selecciona el ultimo. Basandose en que este no tiene fechaHoraFin asignado
    def getEstadoActual(self):
        for cambioEstado in self.cabioEstado.all():
            if cambioEstado.fechaHoraFin==None:
                return cambioEstado.estado.nombre
    
    def new(self, cantVisitantes, fechaYHoraReserva, numeroParaAsignar, fechaHoraActual, duracionReserva, escuela, empleado, sede, estadoParaAsignar, asignacionGuia, exposicionesSeleccionadas):

        self.cantidadAlumnos = cantVisitantes
        self.fechaHoraReserva = fechaYHoraReserva
        self.numeroReserva = numeroParaAsignar
        self.fechaHoraCreacion = fechaHoraActual
        self.duracionEstimada = duracionReserva
        self.escuela = escuela
        self.empleado = empleado
        self.sede = sede
        self.exposicion.add(*exposicionesSeleccionadas)
        self.crearCambioEstado(estadoParaAsignar, fechaHoraActual) #Junto con la creacion de una nueva reserva se crea el cambio de estado
        self.crearAsignaciones(asignacionGuia, fechaYHoraReserva, fechaYHoraReserva+duracionReserva) #Y tambien se crean las asignaciones pertinentes

    def crearCambioEstado(self, estado, fechaHoraActual):
        cambioEstado = CambioEstado.objects.create()
        cambioEstado.new(estado, fechaHoraActual)
        cambioEstado.save()
        self.cabioEstado.add(cambioEstado)
        self.save()

    #Chequea si la reserva esta dentro de una fecha y hora, se utiliza como una parte del metodo para calcular la capacidad de la sede en una fecha y hora dadas
    def estaDentroDeFechaHora(self, fechaHora):
        if self.fechaHoraReserva.replace(tzinfo=None) <= fechaHora and (self.fechaHoraReserva+self.duracionEstimada).replace(tzinfo=None) >= fechaHora:
            return True
        else:
            return False


    def crearAsignaciones(self, asignaciones, fechaHoraInicio, fechaHoraFin):
        for asignacion in asignaciones:
            nuevaAsignacion = AsignacionVisita.objects.create()
            nuevaAsignacion.new(asignacion, fechaHoraInicio, fechaHoraFin)
            nuevaAsignacion.save()
            self.asignacionGuia.add(nuevaAsignacion)
        self.save()

class Sede(models.Model):
    cantMaximaVisitantes = models.IntegerField()
    cantMaxPorGuia = models.IntegerField()
    nombre = models.CharField(max_length= 20)
    exposicion = models.ManyToManyField(Exposicion)
    tarifa = models.ManyToManyField(Tarifa) 
    def getNombre(self):
        return self.nombre
    def obtenerExpTempVigente(self):
        expos = []
        for expo in self.exposicion.all():
            if expo.esTemporal():
                expos.append(expo)
        return expos

    #Realiza la sumatoria de las obras expuestas de las exposiciones seleccionadas dada un tipo de visita seleccionado
    def calcularDuracionDeExposicionesSeleccionadas(self, exposicionSeleccionada):
        duracion = datetime.timedelta(0)
        for exposicion in exposicionSeleccionada:
            duracion += exposicion.calcularDuracionObrasExpuestasPorExpo()
        return duracion
    
    def calcularDuracionCompleta(self, exposicionSeleccionada):
        duracion = datetime.timedelta(0)
        for exposicion in exposicionSeleccionada:
            duracion += exposicion.calcularDuracionObrasExpuestasCompleta()
        return duracion

    def getCantMaximaVisitantes(self):
        return self.cantMaximaVisitantes 


    def buscarGuiasDisponibles(self, dia, fechaHoraInicio, fechaHoraFin):
        empleados = []
        for empleado in Empleado.objects.filter(sedeDondeTrabaja = self): #Filtra y recorre los empleados que trabajan en una sede dada
            tieneAsignaciones = empleado.tieneAsignacionesEnHorario(dia, fechaHoraInicio, fechaHoraFin) #Chequea si el empleado tiene asignaciones
            if tieneAsignaciones != None: #tieneAsignaciones retorna None cuando no es un guia
                if not tieneAsignaciones: #Si no tiene asignaciones
                    empleados.append(empleado.getNombre()) #Lo agrega a la lista de guias
        return empleados

    def getCantMaxPorGuia(self):
        return self.cantMaxPorGuia
    
    #Calcula la cantidad de visitantes en una sede dada una fecha y hora
    def getCantVisitantesFechaHora(self, fechaHora):
        cantVisitantes = 0
        for reserva in ReservaVisita.objects.filter(sede=self):
            if reserva.estaDentroDeFechaHora(fechaHora):
                cantVisitantes += reserva.getCantVisitantes()
        return cantVisitantes
    
    #Utiliza todos los metodos anteriores para verificar que no se sobrepase la capacidad de visitantes ingresados a la capacidad que va a haber para esa fecha y hora
    def verificarCapacidad(self, cantVisitantesNuevos, fechaHora):
        cantVisitantes = self.getCantVisitantesFechaHora(fechaHora) #Obtiene los visitantes que va a haber en esa hora
        cantMaxVisitantes = self.getCantMaximaVisitantes() #obtiene los visitantes maximos que puede haber
        if cantVisitantesNuevos + cantVisitantes > cantMaxVisitantes: #Si la suma de visitantes de otras reservas mas los de esta reserva es mayor a la cantidad maxima
            return False #La capacidad se sobrepasa
        else:
            return True #La capacidad alcanza



# Non persistant classes
from interface import implements, Interface


class IEstrategiaCalculoTiempoReserva(Interface):
    def calcularDuracionDeExposicionesSeleccionadas(self, exposicionSeleccionada, sede):
        pass

class EstrategiaPorExposicion(implements(IEstrategiaCalculoTiempoReserva)):
    def calcularDuracionDeExposicionesSeleccionadas(self, exposicionSeleccionada, sede):
        return sede.calcularDuracionDeExposicionesSeleccionadas(exposicionSeleccionada)

class EstrategiaCompleto(implements(IEstrategiaCalculoTiempoReserva)):
    def calcularDuracionDeExposicionesSeleccionadas(self, exposicionSeleccionada, sede):
        return sede.calcularDuracionCompleta(exposicionSeleccionada)