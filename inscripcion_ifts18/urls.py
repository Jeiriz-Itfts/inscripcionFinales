from django.urls import path, include
from . import views
from .views import *

# que la app sea modular, una app de inscripcion, otra puede ser reportes
app_name = 'inscripcion_ifts18'
urlpatterns = [
    path('',views.index,name='index'),
    path('reset/', views.reset, name='reset'),
    path('alumno/index/',views.check_if_usr, name='check_if_usr'),
    path('reseteado/',views.check_if_mail_exists_and_send_mail, name='check_if_mail_exists_and_send_mail'),
    path('logout/',views.logout, name='logout'),
    path('alumno/inscripcion/',views.inscripcionFinales, name='inscripcionFinales'),
    path('api/alumno', Api.Alumno.as_view(), name='api-alumno'),
    path('api/usuario', Api.Usuario.as_view(), name='api-usr'),
    path('usuario',UsuarioViewSet.as_view({'get':'list','post':'create'}), name='usuario'),
]
