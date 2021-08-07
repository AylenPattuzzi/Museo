from Visita.models import Exposicion, TipoVisita
from django.shortcuts import render
from .models import Estado, Sesion, Escuela, Sede, Tarifa, ReservaVisita
from datetime import datetime
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
    # Datos viejos
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
    return nombreSede # retorna una lista con todos los nombres de las sedes existentes

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
        context = {
        'responsableLogueado': responsableLogueado,
        'escuelaSeleccionada': escuelaSeleccionada,
        'cantVisitantes': cantVisitantes,
        'sedeSeleccionada': sedeSeleccionada,
        'exposicionSeleccionada':expTempVigentes,
        'tipoVisitaSeleccionada': tipoVisitaSeleccionada,
    }    
        return render(request, 'solicitarFechaHoraReserva.html',context)


def buscarExpTempVigentes(sede):
    expTempVigentes = sede.obtenerExpTempVigente()
    return expTempVigentes
#--------------------------------
def tomarSeleccionExposicion(request):
    # datos viejos
    escuelaSeleccionada = request.POST.get('escuelaSeleccionada')
    responsableLogueado = request.POST.get('responsableLogueado')
    cantVisitantes = request.POST.get('cantVisitantes')
    sedeSeleccionada = request.POST.get('sedeSeleccionada')
    tipoVisitaSeleccionada = request.POST.get('tipoVisitaSeleccionada')
    # tomar datos del usuario
    exposicionSeleccionada =  request.POST.getlist('exposicionSeleccionada[]')
    print(exposicionSeleccionada)

    context = {
        'responsableLogueado': responsableLogueado,
        'escuelaSeleccionada': escuelaSeleccionada,
        'cantVisitantes': cantVisitantes,
        'sedeSeleccionada': sedeSeleccionada,
        'tipoVisitaSeleccionada':tipoVisitaSeleccionada,
        'exposicionSeleccionada':exposicionSeleccionada,
    }
    return render(request,"solicitarFechaHoraReserva.html", context)
#---------------------------------

def tomarFechaHoraReserva(request):
    # datos viejos
    escuelaSeleccionada = request.POST.get('escuelaSeleccionada')
    responsableLogueado = request.POST.get('responsableLogueado')
    cantVisitantes = int(request.POST.get('cantVisitantes'))
    sedeSeleccionada = request.POST.get('sedeSeleccionada')
    tipoVisitaSeleccionada = request.POST.get('tipoVisitaSeleccionada')
    listaExposicionesSelec = request.POST.getlist('exposicionSeleccionada[]')
    
    # tomar datos del usuario
    fechaYHoraReserva = request.POST.get('fechaYHoraReserva')
    fechaYHoraReservaParse = parse_datetime(fechaYHoraReserva)

    # mapear objeto sede
    sede = Sede.objects.get(nombre=sedeSeleccionada)

    #mapear objetos expoisicion
    exposicionSeleccionada = []
    for nombreExposicion in listaExposicionesSelec:
        exposicionSeleccionada.append(Exposicion.objects.get(nombre=nombreExposicion))

    duracionReserva = calcularDuracionReserva(tipoVisitaSeleccionada, exposicionSeleccionada, sede)

    if not verificarCapacidad(sede, cantVisitantes):
        context = {
            'responsableLogueado': responsableLogueado,
            'escuelaSeleccionada': escuelaSeleccionada,
            'cantVisitantes': cantVisitantes,
            'sedeSeleccionada': sedeSeleccionada,
            'tipoVisitaSeleccionada':tipoVisitaSeleccionada,
            'exposicionSeleccionada':listaExposicionesSelec,
            'fechaYHoraReserva':fechaYHoraReserva,
            'duracionReserva': duracionReserva,
            'error': "La sede no tiene capacidad para esa cantidad de alumnos en la fecha seleccionada",
        }
        return render(request,"solicitarFechaHoraReserva.html",context)
    dia = 'Lunes' #TODO
    horarioInicio = fechaYHoraReservaParse.time()
    horarioFin = (fechaYHoraReservaParse + duracionReserva).time()
    guiasDisponibles = buscarGuiasDisponibles(sede, dia, horarioInicio, horarioFin)
    cantGuias = calcularCantGuiasNecesarios(sede, cantVisitantes)
    
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
    }
    return render(request,"mostrarGuiasDisponibles.html", context)

def calcularDuracionReserva(tipoVisitaSeleccionada, exposicionSeleccionada, sede):
    duracionReserva = sede.calcularDuracionDeExposicionesSeleccionadas(tipoVisitaSeleccionada, exposicionSeleccionada)
    return duracionReserva

def verificarCapacidad(sede, cantVisitantes):
    tieneCapacidad = sede.verificarCapacidad(cantVisitantes)
    return tieneCapacidad

def buscarGuiasDisponibles(sede, dia, horarioInicio, horarioFin):
    guiasDisponibles = sede.buscarGuiasDisponibles(dia, horarioInicio, horarioFin)
    return guiasDisponibles

def calcularCantGuiasNecesarios(sede, cantVisitantes):
    guiasNecesarios = math.ceil(cantVisitantes / sede.getCantMaxPorGuia())
    return guiasNecesarios

#---------------------------------------------

def tomarSeleccionGuias(request):
    # datos viejos
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
    # datos viejos
    escuelaSeleccionada = request.POST.get('escuelaSeleccionada')
    responsableLogueado = request.POST.get('responsableLogueado')
    cantVisitantes = request.POST.get('cantVisitantes')
    sedeSeleccionada = request.POST.get('sedeSeleccionada')
    tipoVisitaSeleccionada = request.POST.get('tipoVisitaSeleccionada')
    listaExposicionesSelec = request.POST.getlist('exposicionSeleccionada[]')
    fechaYHoraReserva = request.POST.get('fechaYHoraReserva')
    duracionReserva = request.POST.get('duracionReserva')
    cantGuias = request.POST.get('cantGuias')
    horarioInicio = request.POST.get('horarioInicio')
    horarioFin = request.POST.get('horarioFin')
    guiasSeleccionados = request.POST.getlist('guiasSeleccionados[]')

    ReservaVisita.objects.create()
    context = {
        
    }
    return render(request,"finCU.html", context) 

def buscarEstadoParaAsignar(): #TODO cambiar nombre
    for estado in Estado.objects.all():
        if estado.esPendienteDeConfirmacion():
            return estado

def buscarNumeroParaAsignar(reservaVisita):
    numeroParaAsignar = reservaVisita.getNumeroReserva()
    return numeroParaAsignar

def obtenerFechaYHoraActual():
    return datetime.now()
#TODO mirar

#------------------------------------------------