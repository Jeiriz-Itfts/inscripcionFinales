from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Usuario
from django.utils import timezone


def probarExcepcion(request,usuario_id):
    usuarios = get_object_or_404(Usuario, pk=usuario_id) #toma un modelo y numero de arg
    context = {'usuarios': usuarios} #diccionario para pasarle al template
    return render(request, 'inscripcionFinales/usersPlantilla.html',context)


def usersPlantilla(request):
    try:
        usuarios = Usuario.objects.all() #pk=algo_id
        context = {'usuarios': usuarios} #diccionario para pasarle al template
    except Usuario.DoesNotExist:
        raise Http404("No existe el usuario")
    return render(request, 'inscripcionFinales/usersPlantilla.html',context) #el render toma el objeto, nombre plantilla, y diccionario, retorna un Httpresponse

# path('usuario/', views.insertarUsr, name='insertarUsr'),
def insertarUsr(request):
    usuario = Usuario(uid="carlos", password="carlitos", fecha_creacion=timezone.now())
    usuario.save()
    return HttpResponse("Usuario creado: %s " % usuario.uid)

# /usuarios
def getUsrs(request):
    usrsLista = Usuario.objects.all()
    # usrsLista = Usuario.objects.filter(id=2)
    usrsListaFinal = ', '.join([usuario.uid for usuario in usrsLista])
    return HttpResponse(usrsListaFinal)

# Forma 1
# Django permite muchas cosas, usar muchas vistas y devolver muchas cosas pero siempre se debe
# retornar un httpresponse o http404
def getId(request, usuario_id):
    response = "Estas buscando el usuario con uid %s."
    return HttpResponse(response % usuario_id)

# Forma  2
# def getUsr(request, usuario_id):
#    return HttpResponse("Estas buscando el usuario con id %s." % usuario_id)
