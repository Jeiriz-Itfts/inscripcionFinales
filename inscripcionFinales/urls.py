from django.urls import path
from . import views

# que la app sea modular, una app de inscripcion, otra puede ser reportes
app_name = 'inscripcionFinales'
urlpatterns = [
    path('',views.index,name='index'),
    path('reset/', views.reset, name='reset'),
    path('usuario/<int:usuario_id>/', views.get_id, name='get_id'),
    path('insertarUsr/', views.insertar_usr, name='insertar_usr'),
    path('usuarios/',views.get_usrs,name='get_usrs'),
    path('usersPlantilla/',views.users_plantilla, name='users_plantilla'),
    path('<int:usuario_id>/',views.probar_excepcion, name='probar_excepcion')
]
