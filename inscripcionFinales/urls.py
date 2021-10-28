from django.urls import path
from . import views

urlpatterns = [
    path('usuario/<int:usuario_id>/', views.getId, name='getId'),
    path('usuario/', views.insertarUsr, name='insertarUsr'),
    path('usuarios/',views.getUsrs,name='getUsrs'),
    path('',views.usersPlantilla, name='usersPlantilla')
]
