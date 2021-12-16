from django.conf import settings
from django.shortcuts import render
from django.http.response import JsonResponse
from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.utils import timezone
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.template.context import RequestContext
from django import forms
from django.contrib.auth.models import User
from .models import MateriaAlumno, Materia, Curso
import uuid
from django.template.loader import get_template
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMultiAlternatives

# Antes usaba sesiones para saber si estaba logeado
@login_required
def index(request):
    return render(request, 'index.html')

# directivo
@login_required
def curso_materia(request):
    materias = Materia.objects.all()
    cursos = Curso.objects.all()
    return render(request,'directivo/curso_materia.html', {'cursos': cursos,'materias': materias, })

@login_required
def crearCurso(request):
    materias = Materia.objects.all()
    cursos = Curso.objects.all()
    # obtener el nombreCurso luego de hacer un post en el formulario
    if request.method == 'POST':
        nombreCurso = request.POST['nombreCurso']
        # chequear si el curso ya esta creado
        if Curso.objects.filter(descripcion=nombreCurso).exists():
            return render(request,'directivo/curso_materia.html', {'error': "El curso ya está creado!", 'cursos': cursos,'materias': materias})
        curso = Curso.objects.create(descripcion=nombreCurso)
        if curso:
            agregacionCorrecta = True
            return render(request,'directivo/curso_materia.html', {'agregacionCorrecta':agregacionCorrecta, 'cursos': cursos, 'materias': materias})
        return render(request,'directivo/curso_materia.html', {'error': "No se pudo crear el curso",'cursos': cursos, 'materias': materias})
    return render(request,'directivo/curso_materia.html', {'error': "Error formulario", 'cursos': cursos,'materias': materias})
@login_required
def crearMateria(request):
    materias = Materia.objects.all()
    cursos = Curso.objects.all()
    # obtener el nombreCurso luego de hacer un post en el formulario
    if request.method == 'POST':
        nombreCurso = request.POST['desplegableCursos']
        # obtener la materia por medio del formulario
        nombreMateria = request.POST['nombreMateria']
        curso = Curso.objects.get(descripcion=nombreCurso)
        if Materia.objects.filter(descripcion=nombreMateria, id_curso=curso).exists():
            return render(request,'directivo/curso_materia.html', {'error': "Ya existe una materia asociado a ese curso!",'cursos': cursos, 'materias': materias})
        if Materia.objects.filter(descripcion=nombreMateria).exists():
            return render(request,'directivo/curso_materia.html', {'error': "Ya existe una materia con ese nombre!",'cursos': cursos, 'materias': materias})
        else:
            materia = Materia.objects.create(descripcion=nombreMateria, id_curso=curso)
            if materia:
                agregacionCorrecta = True
                return render(request,'directivo/curso_materia.html', {'agregacionCorrecta':agregacionCorrecta, 'cursos': cursos, 'materias': materias})
            else:
                return render(request,'directivo/curso_materia.html', {'error': "No se pudo crear la materia", 'cursos': cursos,'materias': materias})
    return render(request,'directivo/curso_materia.html', {'error': "Error formulario", 'cursos': cursos,'materias': materias})
@login_required
def eliminarCurso(request, id):
    materias = Materia.objects.all()
    cursos = Curso.objects.all()
    if Curso.objects.filter(id=id).delete():
        eliminacionCorrecta = True
        return render(request,'directivo/curso_materia.html', {'eliminacionCorrecta':eliminacionCorrecta, 'cursos': cursos, 'materias': materias})
    return render(request,'directivo/curso_materia.html', {'error': "No se pudo eliminar el curso",'cursos': cursos, 'materias': materias})
@login_required   
def eliminarMateria(request, id):
    materias = Materia.objects.all()
    cursos = Curso.objects.all()
    if Materia.objects.filter(id=id).delete():
        eliminacionCorrecta = True
        return render(request,'directivo/curso_materia.html', {'eliminacionCorrecta':eliminacionCorrecta, 'cursos': cursos, 'materias': materias})
    return render(request,'directivo/curso_materia.html', {'error': "No se pudo eliminar la materia",  'cursos': cursos,'materias': materias})
@login_required
def verInscripcionesDirectivo(request):
    inscripciones = MateriaAlumno.objects.all()
    return render(request,'directivo/ver_inscripciones.html', {'inscripciones': inscripciones})

# alumno
@login_required
def verInscripciones(request):
# obtener id de usuario logueado
    id_usuario = request.user.id
    try: 
        usuario = User.objects.get(pk=id_usuario)
        if usuario:
            inscripciones = MateriaAlumno.objects.filter(user=usuario)
            if inscripciones:
                return render(request,'alumno/inscripciones.html', {'inscripciones': inscripciones})
            return render(request,'alumno/inscripciones.html',  {'inscripciones': inscripciones})
        return render(request,'alumno/inscripciones.html', {'error': "No existe usuario con ese id"})
    except User.DoesNotExist:
        return render(request,'alumno/inscripciones.html', {'error': "No existe usuario con ese id"})


@login_required
def eliminarInscripcion(request, id):
    id_usuario = request.user.id
    usuario = User.objects.get(id=id_usuario)
    inscripciones = MateriaAlumno.objects.filter(user=usuario)
    if MateriaAlumno.objects.filter(pk=id).exists():
        if MateriaAlumno.objects.filter(pk=id).delete():
            eliminacionCorrecta = True
            return render(request,'alumno/inscripciones.html', {'eliminacionCorrecta': eliminacionCorrecta,'inscripciones':inscripciones})
        return render(request,'alumno/inscripciones.html', {'error': 'No se pudo eliminar','inscripciones':inscripciones}) 
    return render(request,'alumno/inscripciones.html', {'error':'No existe la inscripcion','inscripciones':inscripciones})       

@login_required
def inscripcion(request):
    materias = Materia.objects.all()    
    return render(request,'alumno/inscripcion.html', {'materias': materias})

@login_required
def inscribir(request,id):
    materias = Materia.objects.all()
    materia = Materia.objects.get(pk=id)
    id_usuario = request.user.id
    usuario = User.objects.get(id=id_usuario)
    if MateriaAlumno.objects.filter(id_materia=materia, user=usuario).exists():
        return render(request,'alumno/inscripcion.html', {'error': 'Ya esta inscripto a esa materia', 'materias': materias})
    else:
        inscripcion = MateriaAlumno.objects.create(id_materia=materia,user=usuario, fecha_inscripcion=timezone.now())
        if inscripcion:
            inscripcionCorrecta = True
            return render(request,'alumno/inscripcion.html', {'inscripcionCorrecta': inscripcionCorrecta, 'materias': materias})

# Envio de emails y reseteo de pass
def reset(request):
    return render(request, 'reset.html')

def sendMail(email,newPassword, usuario):
    context = {'newPassword': newPassword, 'usuario': usuario}

    template = get_template('correo.html')
    content = template.render(context) #esto hace que sea dinamico y pasarle un valor que permite utilizar en el template, esa vairable, ese valor que le paso
    
    correo = EmailMultiAlternatives(
                'IFTS 18 - Reseteo automático de contraseña',
                'Prueba',
                settings.EMAIL_HOST_USER,
                [email]
                )
    correo.attach_alternative(content, 'text/html') #atach el correo en el template html y el formato
    correo.send() #envia correo
        
def checkMailSendPass(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            #hacer que no se puedan ingresar usuarios duplicados
            # Usuario.objects.filter(mail=mail).exists()
            if User.objects.filter(email=email).exists():
                usuario = User.objects.get(email=email)
                # existe funcion para resetear la contraseña propia de django
                newPassword = str(uuid.uuid4())
                usuario.set_password(newPassword)
                usuario.save()
                try:
                    sendMail(email,newPassword, usuario)
                    return render(request, 'reset.html', {'success': True})
                except Exception as e:
                    return render(request, 'reset.html', {'error': 'No se pudo enviar el correo!'})
            else:
                return render(request, 'reset.html', {'error': 'No existe usuario con ese mail'})
        else:
            return render(request, 'reset.html', {'error': 'No se ingreso mail'})
    else:
        return render(request, 'reset.html',{'error': 'Error, contactarse con soporte.'})


# # Directivos
#     # vista de index
# def cursosMaterias(request):
#     # if request.user.is_authenticated:
#     materias = Materia.objects.all()
#     cursos = Curso.objects.all()
#     return render(request,'directivo/abm/cursos_materias.html',{'cursos':cursos, 'materias': materias})
#     else:
#         return redirect(' :login')    # def curso(request):
#         # agregar un curso a la base de datos
#         if request.session['id_alumno'] is empty:
#             return redirect(' :login')
#         if request.method == 'POST':
#             curso = Curso(nombre=request.POST['nombre'], descripcion=request.POST['descripcion'])
#             curso.save()
#             return redirect(' :abm')
#         materias = Materia.objects.all()
#         cursos = Curso.objects.all()
#         return render(request,'directivo/abm/cursos_materias.html',{'cursos':cursos, 'materias': materias})
        

# # def materia(request):
#     agregar una materia a la base de datos tomando lo que se envió en el formulario cursos_materias.html
#     if request.session['id_alumno'] is empty:
#         return redirect(' :login')
#     if request.method == 'POST':
#         materia = Materia(descripcion=request.POST['descripcion'])
#         materia.save()
#         return redirect(' :abm')
#     materias = Materia.objects.all()
#     cursos = Curso.objects.all()
#     return render(request,'directivo/abm/cursos_materias.html',{'cursos':cursos, 'materias': materias})
    
# def alumno(request):
#     if request.session['id_alumno'] is empty:
#         return redirect(' :login')
#     if request.method == 'POST':
#         alumno = Alumno(nombre=request.POST['nombre'], apellido=request.POST['apellido'], dni=request.POST['dni'])
#         alumno.save()
#         return redirect(' :abm')
#     materias = Materia.objects.all()
#     cursos = Curso.objects.all()
#     return render(request,'directivo/abm/alumnos.html',{'cursos':cursos, 'materias': materias})



# """ All """
# def chequearSiEsUsuario(request):
#     if request.method == 'POST':
#         mail = request.POST.get('mail')
#         if mail:
#             password = request.POST.get('password')
#             if Usuario.objects.filter(mail=mail,password=password).exists():
#                 usuario = Usuario.objects.get(mail=mail)
#                 if Alumno.objects.filter(id_usuario=usuario.id).exists():
#                     alumno = Alumno.objects.get(id_usuario=usuario.id)
#                     request.session['id_alumno'] = alumno.id
#                     request.session['nombre'] = alumno.nombre
#                     return render(request,'alumno/index.html',{'nombre':alumno.nombre})
#                 # chequear si es directivo
#                 elif Directivo.objects.filter(id_usuario=usuario.id).exists():
#                     directivo = Directivo.objects.get(id_usuario=usuario.id)
#                     request.session['id_directivo'] = directivo.id
#                     request.session['nombre'] = directivo.nombre
#                     return render(request,'directivo/index.html',{'nombre':directivo.nombre})
#             return render(request,'login.html',{'error':"El correo o la contraseña son incorrectos!"})
#         return render(request,'login.html',{'error':"No ha introducido una cuenta de correo!"})
#     return render(request,'login.html',{'error':"Error técnico, favor de comunicarse con juan.eiriz@alu.ifts18.edu.com"})



# # """ API """
# # class UsuarioViewSet(ModelViewSet):
# #     def list (self, request):
# #         queryset = Usuario.objects.all()
# #         serializer = UsuarioSeriazer(queryset, many=True)
# #         return JsonResponse(serializer.data, safe=False)
        
# #     def create(self, request):
# #         serializer = UsuarioSeriazer(data=request.data)
# #         if serializer.is_valid():
# #             serializer.save()
# #             return JsonResponse(serializer.data, status=201)
# #         return JsonResponse(serializer.errors, status=400)

# # class MateriaAlumnoViewSet(ModelViewSet):
# #     def list (self, request):
# #         queryset = MateriaAlumno.objects.all()
# #         serializer = MateriaAlumnoSeriazer(queryset, many=True)
# #         return JsonResponse(serializer.data, safe=False)
        
# #     def create(self, request):
# #         serializer = MateriaAlumnoSeriazer(data=request.data)
# #         if serializer.is_valid():
# #             serializer.save()
# #             return JsonResponse(serializer.data, status=201)
# #         return JsonResponse(serializer.errors, status=400)




# # @method_decorator(csrf_exempt, name='dispatch')
# # class Api(View):
# #     @method_decorator(csrf_exempt, name='dispatch')
# #     class Alumno(View):
# #     # '''get all alumnos'''
# #     # def get(self, request):
# #     #     alumnos = Alumno.objects.all()
# #     #     return JsonResponse(list(alumnos.values()), safe=False)   
# #         def post(self, request):
# #             try:
# #                 data = request.POST
# #                 alumno = Alumno()
# #                 alumno.nombre = data['nombre']
# #                 alumno.apellido = data['apellido']
# #                 alumno.legajo = data['legajo']
# #                 alumno.id_usuario = data['id_usuario']
# #                 alumno.id_curso = data['id_curso']
# #                 alumno.dni = data['dni']
# #                 alumno.save()
# #                 return HttpResponse(status=201)
# #             except Exception as e:
# #                 return HttpResponse(e)
    
# #     @method_decorator(csrf_exempt, name='dispatch')
# #     class MateriaAlumno(View):
# #         def post(self, request):
# #             try:
# #                 data = request.POST
# #                 inscripcion = MateriaAlumno()
# #                 inscripcion.id_alumno = data['id_alumno']
# #                 inscripcion.id_materia = data['id_materia']
# #                 inscripcion.fecha_inscripcion = data['fecha_inscripcion']
# #                 inscripcion.save()
# #                 return HttpResponse(status=201)
# #             except Exception as e:
# #                 return HttpResponse(e)

# #         def destroy(self, request):
# #             try:
# #                 data = request.POST
# #                 inscripcion = MateriaAlumno()
# #                 inscripcion.id_materia = data['id_materia']
# #                 inscripcion.id_alumno = data['id_alumno']
# #                 inscripcion.id = data['id']
# #                 inscripcion.delete()
# #                 return HttpResponse(status=201)
# #             except Exception as e:
# #                 return HttpResponse(e)

# #     @method_decorator(csrf_exempt, name='dispatch')
# #     class Usuario(View):
# #         def post(self, request):
# #             try:
# #                 data = request.POST
# #                 usuario = Usuario()
# #                 usuario.uid = data['uid']
# #                 usuario.password = data['password']
# #                 usuario.fecha_creacion = data['fecha_creacion']
# #                 usuario.mail = data['mail']
# #                 usuario.save()
# #                 return HttpResponse('Usuario creado con exito: %s' % usuario.id)
# #             except Exception as e:
# #                 return HttpResponse(e)

# #         def delete(self, request):
# #             try:
# #                 data = self.request.GET
# #                 usuario = get_object_or_404(Usuario, uid=data['uid'])
# #                 usuario.delete()
# #                 return HttpResponse('Usuario eliminado con exito: %s' % usuario.uid)
# #             except Exception as e:
# #                 return HttpResponse(e)
# #     # def get(self, request):
# #     # def put(self, request):
# #     # def delete(self, request):