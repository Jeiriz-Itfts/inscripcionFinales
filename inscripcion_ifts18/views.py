from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from .models import Usuario
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.urls import reverse
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from django.template.context import RequestContext
from django import forms
from .forms import EmailForm

def check_if_mail_exists_and_send_mail(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            email = form.cleaned_data['email']
            return render(request, 'index.html', {'email': email})
            # email = request.GET['email']
            # if email:
            #     if Usuario.objects.filter(email=email).exists():
            #         newPassword=get_random_string(lengh=20)
            #         send_mail(
            #             'IFTS 18 - Reseteo automático de contraseña',
            #             'Se ha creado una nueva contraseña: %s' % newPassword,
            #             'noreply@ifts18.com'
            #             [email],
            #             fail_silently=False,
            #             )
            #     else:
            #         return HttpResponse("El correo no se encuentra registrado!")
        else:
            return HttpResponse("No se ha ingresado un correo")
    else:
        form = EmailForm()
        return render(request, 'index.html', {'form': form})


def index(request):
    return render(request, 'inscripcion_ifts18/index.html')

def reset(request):
    return render(request, 'inscripcion_ifts18/reset.html')

def probar_excepcion(request,usuario_id):
    usuarios = get_object_or_404(Usuario, pk=usuario_id) #toma un modelo y numero de arg
    context = {'usuarios': usuarios} #diccionario para pasarle al template
    return render(request, 'inscripcion_ifts18/usersPlantilla.html',context)


def users_plantilla(request):
    try:
        usuarios = Usuario.objects.all() #pk=algo_id
        context = {'usuarios': usuarios} #diccionario para pasarle al template
    except Usuario.DoesNotExist:
        raise Http404("No existe el usuario")
    return render(request, 'inscripcion_ifts18/usersPlantilla.html',context) #el render toma el objeto, nombre plantilla, y diccionario, retorna un Httpresponse

# path('usuario/', views.insertarUsr, name='insertarUsr'),
def insertar_usr(request):
    usuario = Usuario(uid="carlos", password="carlitos", fecha_creacion=timezone.now())
    usuario.save()
    return HttpResponse("Usuario creado: %s " % usuario.uid)

# /usuarios
def get_usrs(request):
    usrsLista = Usuario.objects.all()
    # usrsLista = Usuario.objects.filter(id=2)
    usrsListaFinal = ', '.join([usuario.uid for usuario in usrsLista])
    return HttpResponse(usrsListaFinal)

# Forma 1
# Django permite muchas cosas, usar muchas vistas y devolver muchas cosas pero siempre se debe
# retornar un httpresponse o http404
def get_id(request, usuario_id):
    response = "Estas buscando el usuario con uid %s."
    return HttpResponse(response % usuario_id)

# Forma  2
# def getUsr(request, usuario_id):
#    return HttpResponse("Estas buscando el usuario con id %s." % usuario_id)
