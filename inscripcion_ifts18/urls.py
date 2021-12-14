

from django.conf.urls import url
from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from .views import *

# que la app sea modular, una app de inscripcion, otra puede ser reportes
app_name = 'inscripcion_ifts18'

# Buenas Practicas arquitectura restfull
urlpatterns = [
    path('accounts/login/',LoginView,{'template_name':'inscripcion_ifts18/login.html'},name='LoginView'),
    path('reset/', reset, name='reset'),
    path('index',chequearSiEsUsuario, name='chequearSiEsUsuario'),
    path('reseteado/',chequearSiMailExisteYEnviarMail, name='chequearSiMailExisteYEnviarMail'),
    path('logout/',LogoutView, name='LogoutView'),
    path('alumno/inscripcion/',Inscripcion.inscripcion, name='inscripcion'),
    path('alumno/inscripciones/',Inscripcion.verInscripciones, name='verInscripciones'),
    path('alumno/inscripciones/<int:id>',Inscripcion.eliminarInscripcion, name='eliminarInscripcion'),
    path('directivo/cursosmaterias',Abm.cursosMaterias, name='cursosMaterias'),
    # url(r'^$', Abm.curso),
    # url(r'^$', Abm.materia),
    # url(r'^$', Abm.alumno),
    path('api/alumno', Api.Alumno.as_view(), name='api-alumno'),
    path('api/usuario', Api.Usuario.as_view(), name='api-usr'),
    path('api/materia', Api.MateriaAlumno.as_view(), name='api-materia'),
    path('alumno/inscripcion/<int:id>',Inscripcion.inscribir, name='inscribir'),
    path('usuario',UsuarioViewSet.as_view({'get':'list','post':'create'}), name='usuario'),
    path('materia',MateriaAlumnoViewSet.as_view({'get':'list','post':'create'}), name='materia'),
]
