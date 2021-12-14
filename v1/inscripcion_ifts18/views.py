from django.http.response import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse, Http404
from django.utils import timezone
from django.urls import reverse
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.template.context import RequestContext
from django import forms
from rest_framework.fields import empty
from rest_framework.serializers import Serializer
from .models import Alumno, Directivo, MateriaAlumno, Usuario, Materia, Curso
from .forms import EmailForm
import uuid
from django.template.loader import get_template
from django.views import View
from django.utils.decorators import method_decorator
from rest_framework.viewsets import ModelViewSet   
from .serializer import UsuarioSeriazer, MateriaAlumnoSeriazer
from django.contrib.auth.decorators import login_required

# class Directivo(object):
#     def __init__(self, nombre, apellido, id_usuario, dni):
#         self.nombre = nombre
#         self.apellido = apellido
#         self.id_usuario = id_usuario
#         self.dni = dni

# class Materia(object):
#     def __init__(self, descripcion):
#         self.descripcion = descripcion


# Alumno
class Inscripcion(View):
    def eliminarInscripcion(request, id):
        try:
            # esto hacerlo con __init__
            id_alumno = request.session['id_alumno']
            inscripcionId = id
            # creo objeto alumno y materia
            if MateriaAlumno.objects.filter(id_alumno=id_alumno, id=inscripcionId).exists():
                if MateriaAlumno.objects.filter(id_alumno=id_alumno,id=inscripcionId).delete():
                    eliminacionCorrecta = True
                    inscripciones = MateriaAlumno.objects.filter(id_alumno=id_alumno)
            return render(request,'inscripcion_ifts18/alumno/inscripciones.html', {'eliminacionCorrecta': eliminacionCorrecta,'inscripciones':inscripciones})
        except Exception as e:
            return HttpResponse(e)

    @login_required
    def verInscripciones(request):
        if request.user.is_authenticated:
            id_alumno = request.session['id_alumno']
            inscripciones = MateriaAlumno.objects.filter(id_alumno=id_alumno)
            return render(request,'inscripcion_ifts18/alumno/inscripciones.html', {'inscripciones': inscripciones})
        else:
            return redirect('inscripcion_ifts18:LoginView')

    # @login_required(login_url="inscripcion_ifts18:login")
    def inscripcion(request):
        if request.user.is_authenticated:
            materias = Materia.objects.all()
            return render(request,'inscripcion_ifts18/alumno/inscripcion.html', {'materias': materias})
        else:
            return redirect('inscripcion_ifts18:LoginView')

    def inscribir(request,id):
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



# Directivos
class Abm(View):
    # vista de index
    def cursosMaterias(request):
        # if request.user.is_authenticated:
        materias = Materia.objects.all()
        cursos = Curso.objects.all()
        return render(request,'inscripcion_ifts18/directivo/abm/cursos_materias.html',{'cursos':cursos, 'materias': materias})
        # else:
        #     return redirect('inscripcion_ifts18:login')

    # def curso(request):
    #     # agregar un curso a la base de datos
    #     if request.session['id_alumno'] is empty:
    #         return redirect('inscripcion_ifts18:login')
    #     if request.method == 'POST':
    #         curso = Curso(nombre=request.POST['nombre'], descripcion=request.POST['descripcion'])
    #         curso.save()
    #         return redirect('inscripcion_ifts18:abm')
    #     materias = Materia.objects.all()
    #     cursos = Curso.objects.all()
    #     return render(request,'inscripcion_ifts18/directivo/abm/cursos_materias.html',{'cursos':cursos, 'materias': materias})
        

    # def materia(request):
    #     # agregar una materia a la base de datos tomando lo que se envió en el formulario cursos_materias.html
    #     if request.session['id_alumno'] is empty:
    #         return redirect('inscripcion_ifts18:login')
    #     if request.method == 'POST':
    #         materia = Materia(descripcion=request.POST['descripcion'])
    #         materia.save()
    #         return redirect('inscripcion_ifts18:abm')
    #     materias = Materia.objects.all()
    #     cursos = Curso.objects.all()
    #     return render(request,'inscripcion_ifts18/directivo/abm/cursos_materias.html',{'cursos':cursos, 'materias': materias})
        

    # def alumno(request):
    #     if request.session['id_alumno'] is empty:
    #         return redirect('inscripcion_ifts18:login')
    #     if request.method == 'POST':
    #         alumno = Alumno(nombre=request.POST['nombre'], apellido=request.POST['apellido'], dni=request.POST['dni'])
    #         alumno.save()
    #         return redirect('inscripcion_ifts18:abm')
    #     materias = Materia.objects.all()
    #     cursos = Curso.objects.all()
    #     return render(request,'inscripcion_ifts18/directivo/abm/alumnos.html',{'cursos':cursos, 'materias': materias})



#     def abmMaterias(request):

    
#     def verCursos(request):

#     def verMaterias(request):



# """ All """
def index(request):
    return render(request,'inscripcion_ifts18/index.html')

def chequearSiEsUsuario(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            return HttpResponse('true')
        # password = request.POST.get('password')
        # if Usuario.objects.filter(mail=mail,password=password).exists():
        #     usuario = Usuario.objects.get(mail=mail)
        #     if Alumno.objects.filter(id_usuario=usuario.id).exists():
        #         alumno = Alumno.objects.get(id_usuario=usuario.id)
        #         request.session['id_alumno'] = alumno.id
        #         request.session['nombre'] = alumno.nombre
        #         return render(request,'inscripcion_ifts18/alumno/index.html',{'nombre':alumno.nombre})
        #     # chequear si es directivo
        #     elif Directivo.objects.filter(id_usuario=usuario.id).exists():
        #         directivo = Directivo.objects.get(id_usuario=usuario.id)
        #         request.session['id_directivo'] = directivo.id
        #         request.session['nombre'] = directivo.nombre
        #         return render(request,'inscripcion_ifts18/directivo/index.html',{'nombre':directivo.nombre})
        else:
            return HttpResponse('false')
        # return render(request,'registration/login.html',{'error':"El correo o la contraseña son incorrectos!"})
    return render(request,'registration/login.html',{'error':"Error técnico, favor de comunicarse con juan.eiriz@alu.ifts18.edu.com"})

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