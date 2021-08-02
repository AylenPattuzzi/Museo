from Visita.models import Exposicion, TipoVisita
from django.shortcuts import render
from .models import Sesion, Escuela, Sede, Tarifa, ReservaVisita

# Create your views here.


def nuevaReserva(request):
    #responsableLogueado = obtenerResponsableLogueado()
    responsableLogueado = "aylen"
    nombreEscuelas = buscarEscuela()
    
    context = {
        'responsableLogueado': responsableLogueado,
        'nombreEscuelas': nombreEscuelas,
    }
    return render(request,"mostrarEscuela.html", context) #mostrar y solicitar selección de escuela

def obtenerResponsableLogueado():
    sesionActiva = Sesion.objects.get(pk=1)  #PENDIENTE
    responsableLogueado = sesionActiva.mostrarResponsable()
    return responsableLogueado

def buscarEscuela():
    nombreEscuelas = []
    for escuela in Escuela.objects.all(): #loop buscar escuelas (mientras haya escuelas)
        nombreEscuelas.append(escuela.getNombre())
    return nombreEscuelas # retorna una lista con los nombres de las ecuelas existentes

#---------------------------------------------

def tomarSeleccionEscuela(request):
    #tomar datos del usuario:
    escuelaSeleccionada = request.POST.get('escuelaSeleccionada')
    
    context = {
        'escuelaSeleccionada': escuelaSeleccionada,
    }
    return render(request,"solicitarCantVisitantes.html", context)

#----------------------------------------------

def tomarCantVisitantes(request):
    #datos previos
    escuelaSeleccionada = request.POST.get('escuelaSeleccionada')
    #tomar datos del usuario:
    cantVisitantes = request.POST.get('cantVisitantes')

    nombreSede = buscarSede()
    context = {
        'nombreSede': nombreSede,
        'escuelaSeleccionada': escuelaSeleccionada,
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
    #tomar datos del usuario:
    sedeSeleccionada = request.POST.get('sedeSeleccionada')

    tipoVisita = buscarTipoVisita()
    context = {
        'tipoVisita': tipoVisita,
        'escuelaSeleccionada': escuelaSeleccionada,
        'cantVisitantes': cantVisitantes,
        'sedeSeleccionada': sedeSeleccionada,
    }
    return render(request,"mostrarTipoVisita.html", context) # muestra la pantalla mostrarTipoVisita

def buscarTipoVisita():
    nombresTipoVisita = []
    for tarifa in Tarifa.objects.all():
        nombresTipoVisita.append(tarifa.obtenerTipoVisita())
    return nombresTipoVisita

#----------------------------------------
def tomarSeleccionTipoVisita(request):
    #datos previos
    escuelaSeleccionada = request.POST.get('escuelaSeleccionada')
    cantVisitantes = request.POST.get('cantVisitantes')
    sedeSeleccionada = request.POST.get('sedeSeleccionada')
    # tomar datos del usuario
    tipoVisitaSeleccionada = request.POST.get('tipoVisitaSeleccionada')
    
    # mapear objeto sede
    sede = Sede.objects.get(nombre=sedeSeleccionada)

    if tipoVisitaSeleccionada.lower() == "por exposición":
        #Selecciona "por exposición" (flujo básico)
        expTempVigentes = buscarExpTempVigentes(sede)
        context = {
            'escuelaSeleccionada': escuelaSeleccionada,
            'cantVisitantes': cantVisitantes,
            'sedeSeleccionada': sedeSeleccionada,
            'tipoVisitaSeleccionada':tipoVisitaSeleccionada,
            'expTempVigentes':expTempVigentes,
        }
        return render(request,"mostrarDatosExposicion.html", context)
    else:
        #selecciona "completo" (flujo alternativo)
        #TODO
        expTempVigentes = buscarExpTempVigentes(sede)
        context = {
            'escuelaSeleccionada': escuelaSeleccionada,
            'cantVisitantes': cantVisitantes,
            'sedeSeleccionada': sedeSeleccionada,
            'tipoVisitaSeleccionada':tipoVisitaSeleccionada,
            'exposicionSeleccionada':expTempVigentes,
        }
        return render(request,"solicitarFechaHoraReserva.html", context)

def buscarExpTempVigentes(sede):
    ExpTempVigente = sede.obtenerExpTempVigente()
    return ExpTempVigente
#--------------------------------
def tomarSeleccionExposicion(request):
    # datos viejos
    escuelaSeleccionada = request.POST.get('escuelaSeleccionada')
    cantVisitantes = request.POST.get('cantVisitantes')
    sedeSeleccionada = request.POST.get('sedeSeleccionada')
    tipoVisitaSeleccionada = request.POST.get('tipoVisitaSeleccionada')
    # tomar datos del usuario
    exposicionSeleccionada =  request.POST.getlist('exposicionSeleccionada[]')
    print(exposicionSeleccionada)

    context = {
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
    cantVisitantes = request.POST.get('cantVisitantes')
    sedeSeleccionada = request.POST.get('sedeSeleccionada')
    tipoVisitaSeleccionada = request.POST.get('tipoVisitaSeleccionada')
    listaExposicionesSelec = request.POST.getlist('exposicionSeleccionada[]')
    
    # tomar datos del usuario
    fechaYHoraReserva = request.POST.get('fechaYHoraReserva')

    # mapear objeto sede
    sede = Sede.objects.get(nombre=sedeSeleccionada)

    #mapear objetos expoisicion
    exposicionSeleccionada = []
    for nombreExposicion in listaExposicionesSelec:
        exposicionSeleccionada.append(Exposicion.objects.get(nombre=nombreExposicion))

    duracionReserva = calcularDuracionReserva(tipoVisitaSeleccionada, exposicionSeleccionada, sede)

    #for reserva in ReservaVisita:
        
    context = {
        'escuelaSeleccionada': escuelaSeleccionada,
        'cantVisitantes': cantVisitantes,
        'sedeSeleccionada': sedeSeleccionada,
        'tipoVisitaSeleccionada':tipoVisitaSeleccionada,
        'exposicionSeleccionada':listaExposicionesSelec,
        'fechaYHoraReserva':fechaYHoraReserva,
        'duracionReserva': duracionReserva,
    }
    return render(request,"mostrarGuiasDisponibles.html", context)

def calcularDuracionReserva(tipoVisitaSeleccionada, exposicionSeleccionada, sede):
    duracionReserva = sede.calcularDuracionDeExposicionesSeleccionadas(tipoVisitaSeleccionada, exposicionSeleccionada)
    return duracionReserva

# incompleto


def buscarEstadoParaAsignar(request):
    context = {}
    return render(request,"base.html", context)


def buscarGuiasDisponibles(request):
    context = {}
    return render(request,"base.html", context)

def buscarNumeroParaAsignar(request):
    context = {}
    return render(request,"base.html", context)





def calcularCantGuiasSegunVisitantes(request):
    context = {}
    return render(request,"base.html", context)

def calcularCantTotalAlumnos(request):
    context = {}
    return render(request,"base.html", context)


def finCu(request):
    context = {}
    return render(request,"base.html", context)

def new(request):
    context = {}
    return render(request,"base.html", context)



def obtenerFechaYHoraActual(request):
    context = {}
    return render(request,"base.html", context)





def tomarConfirmacion(request):
    context = {}
    return render(request,"base.html", context)







def tomarSeleccionGuia(request):
    context = {}
    return render(request,"base.html", context)





def verificarCantMaxVisitantes(request):
    context = {}
    return render(request,"base.html", context)

def verificarCapacidad(total,max):
    if total <= max:
        return True
    else:
        return False