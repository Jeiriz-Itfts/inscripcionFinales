from django.contrib import admin
from .models import Rol,Permiso,Usuario,Directivo,Curso,Alumno,Materia,Materia_Alumno
# Register your models here.
#Poner el modelo aca permite que se edita en el panel de ADMIN

admin.site.register(Rol)
admin.site.register(Permiso)
admin.site.register(Usuario)
admin.site.register(Directivo)
admin.site.register(Curso)
admin.site.register(Alumno)
admin.site.register(Materia)
admin.site.register(Materia_Alumno)
# ahora en admin se pueden ver todos los roles y permisos creados