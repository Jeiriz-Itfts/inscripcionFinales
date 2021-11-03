from django.urls import path
from . import views

# que la app sea modular, una app de inscripcion, otra puede ser reportes
app_name = 'inscripcionFinales'
urlpatterns = [
    path('usuario/<int:usuario_id>/', views.getId, name='getId'),
    path('insertarUsr/', views.insertarUsr, name='insertarUsr'),
    path('usuarios/',views.getUsrs,name='getUsrs'),
    path('usersPlantilla/',views.usersPlantilla, name='usersPlantilla'),
    path('<int:usuario_id>/',views.probarExcepcion, name='probarExcepcion')
]
