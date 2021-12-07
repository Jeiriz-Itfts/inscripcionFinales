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
from .models import Alumno, MateriaAlumno, Usuario, Materia, Curso
from .forms import EmailForm
import uuid
from django.template.loader import get_template
from django.views import View
from django.utils.decorators import method_decorator
from rest_framework.viewsets import ModelViewSet   
from .serializer import UsuarioSeriazer, MateriaAlumnoSeriazer


# class Directivo(object):
#     def __init__(self, nombre, apellido, id_usuario, dni):
#         self.nombre = nombre
#         self.apellido = apellido
#         self.id_usuario = id_usuario
#         self.dni = dni

# class Materia(object):
#     def __init__(self, descripcion):
#         self.descripcion = descripcion

class Inscripcion():
    def eliminarInscripcion(request, id):
        if request.session.get('id_alumno'):
            try:
                id_alumno = request.session['id_alumno']
                inscripcionId = id
                # creo objeto alumno y materia
                inscripcionEliminada = MateriaAlumno.objects.filter(id_alumno=id_alumno, id_materia=inscripcionId).delete()
                if inscripcionEliminada:
                        eliminacionCorrecta = True
                        inscripciones = MateriaAlumno.objects.filter(id_alumno=id_alumno)
                return render(request,'inscripcion_ifts18/alumno/inscripciones.html', {'eliminacionCorrecta': eliminacionCorrecta,'inscripciones':inscripciones})
            except Exception as e:
                return HttpResponse(e)
        else:
            return render(request,'inscripcion_ifts18/index.html')

    def verInscripciones(request):
        if request.session.get('id_alumno'):
            id_alumno = request.session['id_alumno']
            inscripciones = MateriaAlumno.objects.filter(id_alumno=id_alumno)
            return render(request,'inscripcion_ifts18/alumno/inscripciones.html', {'inscripciones': inscripciones})
        else:
            return render(request,'inscripcion_ifts18/index.html')

    def inscripcion(request):
        if  request.session['id_alumno']:
            materias = Materia.objects.all()
            # inscripciones = MateriaAlumno.objects.filter(id_alumno=id_alumno)
            return render(request,'inscripcion_ifts18/alumno/inscripcion.html', {'materias': materias})
        else:
            return render(request,'inscripcion_ifts18/index.html')

    def inscribir(request,id):
        '''recibir el id enviado en inscripcion.html y con ese id, insertar un registro en la tabla MateriaAlumno'''
        if request.session.get('id_alumno'):
            try:
                materias = Materia.objects.all()
                id_materia = id
                id_alumno = request.session['id_alumno']
                # creo objeto alumno y materia
                alumno = Alumno.objects.get(pk=id_alumno)
                materia = Materia.objects.get(pk=id_materia)
                materiaAlumno = MateriaAlumno(id_alumno=alumno, id_materia=materia)
                if MateriaAlumno.objects.filter(id_alumno=alumno, id_materia=materia).exists():
                    return render(request,'inscripcion_ifts18/alumno/inscripcion.html', {'error': 'Ya esta inscripto a esa materia', 'materias': materias})
                # asocio fk con materiaalumno
                else:
                    materiaalumno1 = MateriaAlumno.objects.create(id_materia = materia, id_alumno = alumno, fecha_inscripcion=timezone.now())
                    # creo objeto materiaAlumno
                    if materiaalumno1:
                        inscripto = True
                    return render(request,'inscripcion_ifts18/alumno/inscripcion.html',{'inscripto':inscripto, 'materias': materias})
            except Exception as e:
                return HttpResponse(e)
        else:
            return render(request,'inscripcion_ifts18/index.html')    


# https://docs.djangoproject.com/en/3.2/intro/tutorial02/

""" All """
def alumnoIndex(request):
    if request.session.get('nombre'):
        return render(request,'inscripcion_ifts18/alumno/index.html',{'nombre':request.session.get('nombre')})
    else:
        return render(request,'inscripcion_ifts18/index.html')

def chequearSiEsUsuario(request):
    if request.method == 'POST':
        mail = request.POST.get('mail')
        if mail:
            password = request.POST.get('password')
            if Usuario.objects.filter(mail=mail).exists() & Usuario.objects.filter(password=password).exists():
                usuario = Usuario.objects.get(mail=mail)
                if Alumno.objects.filter(id_usuario=usuario.id).exists():
                    alumno = Alumno.objects.get(id_usuario=usuario.id)
                    request.session['id_alumno'] = alumno.id
                    request.session['nombre'] = alumno.nombre
                    inscripciones = Inscripcion()
                    inscripciones.inscripcion()
                return HttpResponse("El usuario no es alumno")
            return HttpResponse("El usuario con el mail %s no existe" % mail)
        return HttpResponse("No se ha introducido ningún correo")
    return HttpResponse("404")

def login(request):
    return render(request, 'inscripcion_ifts18/login.html')

def reset(request):
    return render(request, 'inscripcion_ifts18/reset.html')

def sendMail(self, mail, newPassword):
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
        
def chequearSiMailExisteYEnviarMail(self, request):
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
                    self.sendMail(mail, newPassword)
                    return render(request, 'inscripcion_ifts18/reseteado.html')
            except Usuario.DoesNotExist:
                return HttpResponse("El correo no se encuentra registrado!")
        return HttpResponse("No se ha introducido ningún correo")
    return render(request, 'inscripcion_ifts18/reset.html')

def logout(request):
    if request.session.get('nombre') is not None:
        del request.session['nombre']
    if request.session.get('id_alumno') is not None:
        del request.session['id_alumno']
    return render(request,'inscripcion_ifts18/index.html')

""" API """
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

class MateriaAlumnoViewSet(ModelViewSet):
    def list (self, request):
        queryset = MateriaAlumno.objects.all()
        serializer = MateriaAlumnoSeriazer(queryset, many=True)
        return JsonResponse(serializer.data, safe=False)
        
    def create(self, request):
        serializer = MateriaAlumnoSeriazer(data=request.data)
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
    class MateriaAlumno(View):
        def post(self, request):
            try:
                data = request.POST
                inscripcion = MateriaAlumno()
                inscripcion.id_alumno = data['id_alumno']
                inscripcion.id_materia = data['id_materia']
                inscripcion.fecha_inscripcion = data['fecha_inscripcion']
                inscripcion.save()
                return HttpResponse(status=201)
            except Exception as e:
                return HttpResponse(e)

        def destroy(self, request):
            try:
                data = request.POST
                inscripcion = MateriaAlumno()
                inscripcion.id_materia = data['id_materia']
                inscripcion.id_alumno = data['id_alumno']
                inscripcion.id = data['id']
                inscripcion.delete()
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