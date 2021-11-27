from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from django.utils import timezone
from django.urls import reverse
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.template.context import RequestContext
from django import forms
from .models import Alumno, Usuario
from .forms import EmailForm
import uuid
from django.template.loader import get_template

#get_template de template loader

def inscripcionFinales(request):
    return render(request,'inscripcion_ifts18/alumno/inscripcion.html')

def logout(request):
    return render(request,'inscripcion_ifts18/alumno/logout.html')



def sendMail(mail, newPassword):
    context = {'newPassword': newPassword}
    template = get_template('inscripcion_ifts18/correo.html')
    content = template.render(context) #esto hace que sea dinamico y pasarle un valor que permite utilizar en el template, esa vairable, ese valor que le paso

    email = EmailMultiAlternatives(
                  'IFTS 18 - Reseteo automático de contraseña',
                  settings.EMAIL_HOST_USER,
                  [mail]
                  )
    email.attach_alternative(content, "text/html") #atach el correo en el template html y el formato
    try:
        email.send() #envia correo
    except:
        return HttpResponse("Error al enviar correo")

def check_if_mail_exists_and_send_mail(request):
    if request.method == 'POST':
        mail = request.POST.get('mail')
        if mail:
            try:
                #hacer que no se puedan ingresar usuarios duplicados
                Usuario.objects.filter(mail=mail).exists()
                usuario = Usuario.objects.get(mail=mail)
                if usuario.mail:
                    newPassword = str(uuid.uuid4())
                    usuario.password = newPassword
                    usuario.save()
                    sendMail(mail, newPassword)
                    return render(request, 'inscripcion_ifts18/reseteado.html')
            except Usuario.DoesNotExist:
                return HttpResponse("El correo no se encuentra registrado!")
        return HttpResponse("No se ha introducido ningún correo")
    return render(request, 'inscripcion_ifts18/reset.html')



def check(request):
    if request.method == 'POST':
        mail = request.POST.get('mail')
        if mail:
            password = request.POST.get('password')
            if Usuario.objects.filter(mail=mail).exists() & Usuario.objects.filter(password=password).exists():
                usuario = Usuario.objects.get(mail=mail)
                id = usuario.id
                """ mail duplicado """
                if Alumno.objects.filter(id_usuario=id).exists():
                    alumno = Alumno.objects.get(id_usuario=id)
                    return render(request, 'inscripcion_ifts18/alumno/index.html', {'nombre': alumno.nombre})
                return HttpResponse("El usuario no es alumno")
            return HttpResponse("El usuario con el mail %s no existe" % mail)
        return HttpResponse("No se ha introducido ningún correo")
    return HttpResponse("404")

def index(request):
    return render(request, 'inscripcion_ifts18/index.html')

def reset(request):
    return render(request, 'inscripcion_ifts18/reset.html')

# def probar_excepcion(request,usuario_id):
#     usuarios = get_object_or_404(Usuario, pk=usuario_id) #toma un modelo y numero de arg
#     context = {'usuarios': usuarios} #diccionario para pasarle al template
#     return render(request, 'inscripcion_ifts18/usersPlantilla.html',context)


# def users_plantilla(request):
#     try:
#         usuarios = Usuario.objects.all() #pk=algo_id
#         context = {'usuarios': usuarios} #diccionario para pasarle al template
#     except Usuario.DoesNotExist:
#         raise Http404("No existe el usuario")
#     return render(request, 'inscripcion_ifts18/usersPlantilla.html',context) #el render toma el objeto, nombre plantilla, y diccionario, retorna un Httpresponse

# path('usuario/', views.insertarUsr, name='insertarUsr'),
# def insertar_usr(request):
#     usuario = Usuario(uid="carlos", password="carlitos", fecha_creacion=timezone.now())
#     usuario.save()
#     return HttpResponse("Usuario creado: %s " % usuario.uid)

# /usuarios
# def get_usrs(request):
#     usrsLista = Usuario.objects.all()
#     # usrsLista = Usuario.objects.filter(id=2)
#     usrsListaFinal = ', '.join([usuario.uid for usuario in usrsLista])
#     return HttpResponse(usrsListaFinal)

# Forma 1
# Django permite muchas cosas, usar muchas vistas y devolver muchas cosas pero siempre se debe
# retornar un httpresponse o http404
# def get_id(request, usuario_id):
#     response = "Estas buscando el usuario con uid %s."
#     return HttpResponse(response % usuario_id)

# Forma  2
# def getUsr(request, usuario_id):
#    return HttpResponse("Estas buscando el usuario con id %s." % usuario_id)
