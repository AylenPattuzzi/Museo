"""Museo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from . import views

app_name='visita'

urlpatterns = [
    path('index/', views.index),
    path('nuevaReserva/', views.nuevaReserva),
    path('tomarCantVisitantes/', views.tomarCantVisitantes),
    path('tomarConfirmacion/', views.tomarConfirmacion),
    path('tomarFechaHoraReserva/', views.tomarFechaHoraReserva),
    path('tomarSeleccionEscuela/', views.tomarSeleccionEscuela),
    path('tomarSeleccionExposicion/', views.tomarSeleccionExposicion),
    path('tomarSeleccionGuias/', views.tomarSeleccionGuias),
    path('tomarSeleccionSede/', views.tomarSeleccionSede),
    path('tomarSeleccionTipoVisita/', views.tomarSeleccionTipoVisita),
]
