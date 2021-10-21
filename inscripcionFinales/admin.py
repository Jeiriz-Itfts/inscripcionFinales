from django.contrib import admin
from .models import Rol,Permiso
# Register your models here.
#Poner el modelo aca permite que se edita en el panel de ADMIN

admin.site.register(Rol)
admin.site.register(Permiso)
# ahora en admin se pueden ver todos los roles y permisos creados