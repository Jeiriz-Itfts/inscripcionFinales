

from django.conf.urls import url
from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from .views import *

# que la app sea modular, una app de inscripcion, otra puede ser reportes
app_name = 'inscripcion_ifts18'

# Buenas Practicas arquitectura restfull
urlpatterns = [
    path('',LoginView.as_view(),name='login'),
    path('logout/',LogoutView.as_view(), name='logout'),
    path('index/',index, name='index'),
    path('alumno/inscripcion/',inscripcion, name='inscripcion'),
    path('alumno/inscripciones/',verInscripciones, name='verInscripciones'),
    path('alumno/inscripciones/<int:id>',eliminarInscripcion, name='eliminarInscripcion'),
    path('alumno/inscripcion/<int:id>',inscribir, name='inscribir'),
    path('directivo/curso_materia/',curso_materia, name='curso_materia'),
    path('directivo/curso_materia/curso/',crearCurso, name='crearCurso'),
    path('directivo/curso_materia/curso/<int:id>',eliminarCurso, name='eliminarCurso'),
    path('directivo/curso_materia/materia/',crearMateria, name='crearMateria'),
    path('directivo/curso_materia/materia/<int:id>',eliminarMateria, name='eliminarMateria'),
    path('directivo/inscripciones/',verInscripcionesDirectivo, name='verInscripcionesDirectivo')
    # path('reset/', reset, name='reset'),
    # path('reseteado/',chequearSiMailExisteYEnviarMail, name='chequearSiMailExisteYEnviarMail'),
    # path('directivo/cursosmaterias',Abm.cursosMaterias, name='cursosMaterias'),
    # url(r'^$', Abm.curso),
    # url(r'^$', Abm.materia),
    # url(r'^$', Abm.alumno),
    # path('api/alumno', Api.Alumno.as_view(), name='api-alumno'),
    # path('api/usuario', Api.Usuario.as_view(), name='api-usr'),
    # path('api/materia', Api.MateriaAlumno.as_view(), name='api-materia'),

    # path('usuario',UsuarioViewSet.as_view({'get':'list','post':'create'}), name='usuario'),
    # path('materia',MateriaAlumnoViewSet.as_view({'get':'list','post':'create'}), name='materia'),
]
