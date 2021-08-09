from Visita.models import Exposicion, TipoVisita
from django.shortcuts import render
from .models import Estado, Sesion, Escuela, Sede, Tarifa, ReservaVisita, Empleado, AsignacionVisita
from datetime import datetime, timedelta
from django.utils.dateparse import parse_datetime
import math

# Create your views here.
def index(request):
    return render(request,"index.html", {})


def nuevaReserva(request):
    responsableLogueado = obtenerResponsableLogueado(int(request.POST.get('sesion')))
    
    
    nombreEscuelas = buscarEscuela()
    
    context = {
        'responsableLogueado': responsableLogueado,
        'nombreEscuelas': nombreEscuelas,
    }
    return render(request,"mostrarEscuela.html", context) #mostrar y solicitar selección de escuela

def obtenerResponsableLogueado(sesion):
    sesionActiva = Sesion.objects.get(pk=sesion)
    responsableLogueado = sesionActiva.mostrarResponsable()
    return responsableLogueado

def buscarEscuela():
    nombreEscuelas = []
    for escuela in Escuela.objects.all(): #loop buscar escuelas (mientras haya escuelas)
        nombreEscuelas.append(escuela.getNombre())
    return nombreEscuelas # retorna una lista con los nombres de las ecuelas existentes

#---------------------------------------------

def tomarSeleccionEscuela(request):
    # datos previos
    responsableLogueado = request.POST.get('responsableLogueado')
    # tomar datos del usuario:
    escuelaSeleccionada = request.POST.get('escuelaSeleccionada')

    
    context = {
        'responsableLogueado': responsableLogueado,
        'escuelaSeleccionada': escuelaSeleccionada,
    }
    return render(request,"solicitarCantVisitantes.html", context)

#----------------------------------------------

def tomarCantVisitantes(request):
    #datos previos
    escuelaSeleccionada = request.POST.get('escuelaSeleccionada')
    responsableLogueado = request.POST.get('responsableLogueado')

    #tomar datos del usuario:
    cantVisitantes = request.POST.get('cantVisitantes')

    nombreSede = buscarSede()

    context = {
        'nombreSede': nombreSede,
        'escuelaSeleccionada': escuelaSeleccionada,
        'responsableLogueado': responsableLogueado,
        'cantVisitantes': cantVisitantes,
    }
    return render(request,"mostrarSede.html", context) #mostrar pantalla mostrarSede

def buscarSede():
    nombreSede = []
    for sede in Sede.objects.all(): #loop nombre Sede (mientras haya sedes)
        nombreSede.append(sede.getNombre())
    return nombreSede # retorna una lista con los nombres de las sedes existentes

# ---------------------------------

def tomarSeleccionSede(request):
    #datos previos:
    escuelaSeleccionada = request.POST.get('escuelaSeleccionada')
    cantVisitantes = request.POST.get('cantVisitantes')
    responsableLogueado = request.POST.get('responsableLogueado')
    #tomar datos del usuario:
    sedeSeleccionada = request.POST.get('sedeSeleccionada')

    tipoVisita = buscarTipoVisita()
    context = {
        'responsableLogueado': responsableLogueado,
        'tipoVisita': tipoVisita,
        'escuelaSeleccionada': escuelaSeleccionada,
        'cantVisitantes': cantVisitantes,
        'sedeSeleccionada': sedeSeleccionada,
    }
    return render(request,"mostrarTipoVisita.html", context) # muestra la pantalla mostrarTipoVisita

def buscarTipoVisita():
    nombresTipoVisita = []
    for tarifa in Tarifa.objects.all():
        tipoVisita = tarifa.obtenerTipoVisita()
        if not tipoVisita in nombresTipoVisita:
            nombresTipoVisita.append(tipoVisita)
    return nombresTipoVisita

#----------------------------------------
def tomarSeleccionTipoVisita(request):
    #datos previos:
    escuelaSeleccionada = request.POST.get('escuelaSeleccionada')
    cantVisitantes = request.POST.get('cantVisitantes')
    responsableLogueado = request.POST.get('responsableLogueado')
    sedeSeleccionada = request.POST.get('sedeSeleccionada')
    #tomar datos del usuario:
    tipoVisitaSeleccionada = request.POST.get('tipoVisitaSeleccionada')

    sede = Sede.objects.get(nombre = sedeSeleccionada)
    expTempVigentes = buscarExpTempVigentes(sede)
    
    if tipoVisitaSeleccionada.lower() == 'por exposicion':

        context = {
        'responsableLogueado': responsableLogueado,
        'escuelaSeleccionada': escuelaSeleccionada,
        'cantVisitantes': cantVisitantes,
        'sedeSeleccionada': sedeSeleccionada,
        'tipoVisitaSeleccionada': tipoVisitaSeleccionada,
        'expTempVigentes': expTempVigentes,
    }
        return render(request, 'mostrarDatosExposicion.html',context)
    else:
        expoNombres=[]
        for expo in expTempVigentes:
            expoNombres.append(expo.nombre)
        context = {
        'responsableLogueado': responsableLogueado,
        'escuelaSeleccionada': escuelaSeleccionada,
        'cantVisitantes': cantVisitantes,
        'sedeSeleccionada': sedeSeleccionada,
        'exposicionSeleccionada':expoNombres,
        'tipoVisitaSeleccionada': tipoVisitaSeleccionada,
    }    
        return render(request, 'solicitarFechaHoraReserva.html',context)


def buscarExpTempVigentes(sede):
    expTempVigentes = sede.obtenerExpTempVigente()
    return expTempVigentes
#--------------------------------
def tomarSeleccionExposicion(request, error=False):
    # datos previos
    escuelaSeleccionada = request.POST.get('escuelaSeleccionada')
    responsableLogueado = request.POST.get('responsableLogueado')
    cantVisitantes = request.POST.get('cantVisitantes')
    sedeSeleccionada = request.POST.get('sedeSeleccionada')
    tipoVisitaSeleccionada = request.POST.get('tipoVisitaSeleccionada')
    # tomar datos del usuario
    exposicionSeleccionada =  request.POST.getlist('exposicionSeleccionada[]')
    print(exposicionSeleccionada)

    msgError = ''
    if error:
        msgError = 'No hay suficientes guías disponibles para la fecha y hora seleccionada.'

    context = {
        'responsableLogueado': responsableLogueado,
        'escuelaSeleccionada': escuelaSeleccionada,
        'cantVisitantes': cantVisitantes,
        'sedeSeleccionada': sedeSeleccionada,
        'tipoVisitaSeleccionada':tipoVisitaSeleccionada,
        'exposicionSeleccionada':exposicionSeleccionada,
        'error':msgError
    }
    return render(request,"solicitarFechaHoraReserva.html", context)
#---------------------------------

def tomarFechaHoraReserva(request, error = False):
    # datos previos
    escuelaSeleccionada = request.POST.get('escuelaSeleccionada')
    responsableLogueado = request.POST.get('responsableLogueado')
    cantVisitantes = int(request.POST.get('cantVisitantes'))
    sedeSeleccionada = request.POST.get('sedeSeleccionada')
    tipoVisitaSeleccionada = request.POST.get('tipoVisitaSeleccionada')
    listaExposicionesSelec = request.POST.getlist('exposicionSeleccionada[]')
    guiasSeleccionados = request.POST.getlist('guiasSeleccionados[]')
    
    # tomar datos del usuario
    fechaYHoraReserva = request.POST.get('fechaYHoraReserva')
    fechaYHoraReservaParse = parse_datetime(fechaYHoraReserva).replace(tzinfo=None)

    # mapear objeto sede
    sede = Sede.objects.get(nombre=sedeSeleccionada)

    #mapear objetos expoisicion
    exposicionSeleccionada = []
    for nombreExposicion in listaExposicionesSelec:
        exposicionSeleccionada.append(Exposicion.objects.get(nombre=nombreExposicion))

    duracionReserva = calcularDuracionReserva(tipoVisitaSeleccionada, exposicionSeleccionada, sede)

    if not verificarCapacidad(sede, cantVisitantes, fechaYHoraReservaParse):
        context = {
            'responsableLogueado': responsableLogueado,
            'escuelaSeleccionada': escuelaSeleccionada,
            'cantVisitantes': cantVisitantes,
            'sedeSeleccionada': sedeSeleccionada,
            'tipoVisitaSeleccionada':tipoVisitaSeleccionada,
            'exposicionSeleccionada':listaExposicionesSelec,
            'fechaYHoraReserva':fechaYHoraReserva,
            'duracionReserva': duracionReserva,
            'error': "La sede no tiene capacidad para esa cantidad de alumnos en la fecha seleccionada.",
        }
        return render(request,"solicitarFechaHoraReserva.html",context)
    dia = fechaYHoraReservaParse.weekday()
    if dia == 0:
        dia = "lunes"
    elif dia == 1:
        dia = "martes"
    elif dia == 2:
        dia = "miercoles"
    elif dia == 3:
        dia = "jueves"
    elif dia == 4:
        dia = "viernes"
    elif dia == 5:
        dia = "sabado"
    elif dia == 6:
        dia = "domingo"
    
    
    horarioInicio = fechaYHoraReservaParse.time()
    horarioFin = (fechaYHoraReservaParse + duracionReserva).time()
    guiasDisponibles = buscarGuiasDisponibles(sede, dia, fechaYHoraReservaParse, (fechaYHoraReservaParse+duracionReserva))
    cantGuias = calcularCantGuiasNecesarios(sede, cantVisitantes)
    if cantGuias > len(guiasDisponibles):
        return tomarSeleccionExposicion(request, True)
    msgError = ''
    if error:
        msgError = 'Seleccione la cantidad de guías exacta.'
    context = {
        'responsableLogueado': responsableLogueado,
        'escuelaSeleccionada': escuelaSeleccionada,
        'cantVisitantes': cantVisitantes,
        'sedeSeleccionada': sedeSeleccionada,
        'tipoVisitaSeleccionada':tipoVisitaSeleccionada,
        'exposicionSeleccionada':listaExposicionesSelec,
        'fechaYHoraReserva':fechaYHoraReserva,
        'duracionReserva': duracionReserva,
        'guiasDisponibles': guiasDisponibles,
        'cantGuias': cantGuias,
        'horarioInicio': horarioInicio,
        'horarioFin': horarioFin,
        'error': msgError,
    }
    return render(request,"mostrarGuiasDisponibles.html", context)

def calcularDuracionReserva(tipoVisitaSeleccionada, exposicionSeleccionada, sede):
    duracionReserva = sede.calcularDuracionDeExposicionesSeleccionadas(tipoVisitaSeleccionada, exposicionSeleccionada)
    return duracionReserva

def verificarCapacidad(sede, cantVisitantes, fechaHora):
    tieneCapacidad = sede.verificarCapacidad(cantVisitantes, fechaHora)
    return tieneCapacidad

def buscarGuiasDisponibles(sede, dia, fechaHoraInicio, fechaHoraFin):
    guiasDisponibles = sede.buscarGuiasDisponibles(dia, fechaHoraInicio, fechaHoraFin)
    return guiasDisponibles

def calcularCantGuiasNecesarios(sede, cantVisitantes):
    guiasNecesarios = math.ceil(cantVisitantes / sede.getCantMaxPorGuia())
    return guiasNecesarios

#---------------------------------------------

def tomarSeleccionGuias(request):
    # datos previos
    escuelaSeleccionada = request.POST.get('escuelaSeleccionada')
    responsableLogueado = request.POST.get('responsableLogueado')
    cantVisitantes = int(request.POST.get('cantVisitantes'))
    sedeSeleccionada = request.POST.get('sedeSeleccionada')
    tipoVisitaSeleccionada = request.POST.get('tipoVisitaSeleccionada')
    listaExposicionesSelec = request.POST.getlist('exposicionSeleccionada[]')
    fechaYHoraReserva = request.POST.get('fechaYHoraReserva')
    duracionReserva = request.POST.get('duracionReserva')
    cantGuias = request.POST.get('cantGuias')
    horarioInicio = request.POST.get('horarioInicio')
    horarioFin = request.POST.get('horarioFin')
    # tomar datos del usuario
    guiasSeleccionados = request.POST.getlist('guiasSeleccionados[]')

    if not len(guiasSeleccionados)== int(cantGuias):
        return tomarFechaHoraReserva(request, True)



    context = {
        'responsableLogueado': responsableLogueado,
        'escuelaSeleccionada': escuelaSeleccionada,
        'cantVisitantes': cantVisitantes,
        'sedeSeleccionada': sedeSeleccionada,
        'tipoVisitaSeleccionada':tipoVisitaSeleccionada,
        'exposicionSeleccionada':listaExposicionesSelec,
        'fechaYHoraReserva':fechaYHoraReserva,
        'duracionReserva': duracionReserva,
        'cantGuias': cantGuias,
        'horarioInicio': horarioInicio,
        'horarioFin': horarioFin,
        'guiasSeleccionados': guiasSeleccionados,
    }
    return render(request, 'solicitarConfirmacion.html', context)
#-------------------------------
def tomarConfirmacion(request):
    # datos para generar una nueva reserva
    cantVisitantes = int(request.POST.get('cantVisitantes'))
    fechaYHoraReserva = parse_datetime(request.POST.get('fechaYHoraReserva'))
    numeroParaAsignar = buscarNumeroParaAsignar()
    fechaHoraActual = obtenerFechaYHoraActual()
    duracionReserva = datetime.strptime(request.POST.get('duracionReserva'), '%H:%M:%S')
    duracionReserva = timedelta(hours=duracionReserva.hour, minutes=duracionReserva.minute, seconds=duracionReserva.second)

    # Datos que deben Mapearse -----------------------------------------------
    escuelaSeleccionada = request.POST.get('escuelaSeleccionada')
    escuela = Escuela.objects.get(nombre=escuelaSeleccionada)
    responsableLogueado = request.POST.get('responsableLogueado')
    responsableLogueado = responsableLogueado.split(", ")
    empleado = Empleado.objects.get(apellido= responsableLogueado[0], nombre=responsableLogueado[1])
    sedeSeleccionada = request.POST.get('sedeSeleccionada')
    sede = Sede.objects.get(nombre=sedeSeleccionada)
    estadoParaAsignar = buscarEstadoParaAsignar()

    guiasSeleccionados = request.POST.getlist('guiasSeleccionados[]')
    asignacionGuia = []
    for guia  in guiasSeleccionados:
        guia = guia.split(", ")
        asignacionGuia.append(Empleado.objects.get(apellido=guia[0] ,nombre = guia[1]))
    
    listaExposicionesSelec = request.POST.getlist('exposicionSeleccionada[]')
    exposicionesSeleccionadas = []
    for exposicion in listaExposicionesSelec:
        exposicionesSeleccionadas.append(Exposicion.objects.get(nombre=exposicion))

    # datos viejos que no se usan para crear la reserva (se pueden mostrar en la pantalla final)
    horarioInicio = request.POST.get('horarioInicio')
    horarioFin = request.POST.get('horarioFin')
    cantGuias = request.POST.get('cantGuias')
    tipoVisitaSeleccionada = request.POST.get('tipoVisitaSeleccionada')
    
    

    nuevaReserva = ReservaVisita.objects.create()
    nuevaReserva.new(
        cantVisitantes,
        fechaYHoraReserva,
        numeroParaAsignar,
        fechaHoraActual,
        duracionReserva,
        escuela,
        empleado,
        sede,
        estadoParaAsignar,
        asignacionGuia,
        exposicionesSeleccionadas
    )

    nuevaReserva.save()
    

    context = {
        'reserva': nuevaReserva,
    }
    #return JsonResponse(serializers.serialize('json', [nuevaReserva,]), safe=False)
    return render(request,"finCU.html", context) 

def buscarEstadoParaAsignar():
    for estado in Estado.objects.all():
        if estado.esPendienteDeConfirmacion():
            return estado

def buscarNumeroParaAsignar():
    maxNumeroReserva = 0
    for reserva in ReservaVisita.objects.all():
        try:
            if maxNumeroReserva < reserva.getNumeroReserva():
                maxNumeroReserva = reserva.getNumeroReserva()
        except:
            pass
    return maxNumeroReserva + 1

def obtenerFechaYHoraActual():
    return datetime.now()

#------------------------------------------------