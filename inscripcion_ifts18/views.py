from django.http.response import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from django.utils import timezone
from django.urls import reverse
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.template.context import RequestContext
from django import forms
from rest_framework.serializers import Serializer
from .models import Alumno, Usuario
from .forms import EmailForm
import uuid
from django.template.loader import get_template
from django.views import View
from django.utils.decorators import method_decorator
from rest_framework.viewsets import ModelViewSet   
from .serializer import UsuarioSeriazer



class UsuarioViewSet(ModelViewSet):
    def list (self, request):
        queryset = Usuario.objects.all()
        serializer = UsuarioSeriazer(queryset, many=True)
        return JsonResponse(serializer.data, safe=False)
        
    def create(self, request):
        serializer = UsuarioSeriazer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)




@method_decorator(csrf_exempt, name='dispatch')
class Api(View):
    @method_decorator(csrf_exempt, name='dispatch')
    class Alumno(View):
    # '''get all alumnos'''
    # def get(self, request):
    #     alumnos = Alumno.objects.all()
    #     return JsonResponse(list(alumnos.values()), safe=False)   
        def post(self, request):
            try:
                data = request.POST
                alumno = Alumno()
                alumno.nombre = data['nombre']
                alumno.apellido = data['apellido']
                alumno.legajo = data['legajo']
                alumno.id_usuario = data['id_usuario']
                alumno.id_curso = data['id_curso']
                alumno.dni = data['dni']
                alumno.save()
                return HttpResponse(status=201)
            except Exception as e:
                return HttpResponse(e)

    @method_decorator(csrf_exempt, name='dispatch')
    class Usuario(View):
        def post(self, request):
            try:
                data = request.POST
                usuario = Usuario()
                usuario.uid = data['uid']
                usuario.password = data['password']
                usuario.fecha_creacion = data['fecha_creacion']
                usuario.mail = data['mail']
                usuario.save()
                return HttpResponse('Usuario creado con exito: %s' % usuario.id)
            except Exception as e:
                return HttpResponse(e)

        def delete(self, request):
            try:
                data = self.request.GET
                usuario = get_object_or_404(Usuario, uid=data['uid'])
                usuario.delete()
                return HttpResponse('Usuario eliminado con exito: %s' % usuario.uid)
            except Exception as e:
                return HttpResponse(e)
    # def get(self, request):
    # def put(self, request):
    # def delete(self, request):
        



# class Alumno(View):
#     def inscribirFinales(self, request):


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



def check_if_usr(request):
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
