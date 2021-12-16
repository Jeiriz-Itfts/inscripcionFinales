"""miProyecto URL Configuration

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
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from inscripcionFinales.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/',LoginView.as_view(),name='login'),
    path('logout/',LogoutView.as_view(), name='logout'),
    path('',index, name='index'),
    path('alumno/inscripcion/',inscripcion, name='inscripcion'),
    path('alumno/inscripciones/',verInscripciones, name='verInscripciones'),
    path('alumno/inscripciones/<int:id>',eliminarInscripcion, name='eliminarInscripcion'),
    path('alumno/inscripcion/<int:id>',inscribir, name='inscribir'),
    path('directivo/curso_materia/',curso_materia, name='curso_materia'),
    path('directivo/curso_materia/curso/',crearCurso, name='crearCurso'),
    path('directivo/curso_materia/curso/<int:id>',eliminarCurso, name='eliminarCurso'),
    path('directivo/curso_materia/materia/',crearMateria, name='crearMateria'),
    path('directivo/curso_materia/materia/<int:id>',eliminarMateria, name='eliminarMateria'),
    path('directivo/inscripciones/',verInscripcionesDirectivo, name='verInscripcionesDirectivo'),
    path('reset/', reset, name='reset'),
    path('reseteado/',checkMailSendPass, name='checkMailSendPass')
]
    # url(r'^$', Abm.curso),
    # url(r'^$', Abm.materia),
    # url(r'^$', Abm.alumno),
    # path('api/alumno', Api.Alumno.as_view(), name='api-alumno'),
    # path('api/usuario', Api.Usuario.as_view(), name='api-usr'),
    # path('api/materia', Api.MateriaAlumno.as_view(), name='api-materia'),

    # path('usuario',UsuarioViewSet.as_view({'get':'list','post':'create'}), name='usuario'),
    # path('materia',MateriaAlumnoViewSet.as_view({'get':'list','post':'create'}), name='materia')