from django.contrib import admin
from .models import Rol,Permiso,Usuario,Directivo,Curso,Alumno,Materia,MateriaAlumno
# Register your models here.
#Poner el modelo aca permite que se edita en el panel de ADMIN
# aca podes hacer que no aparezca ciertos campos seteados en models.py
# ya aparecen las FK en admin
#stack in line ocupa mucho espacio, por eso se usa tabular

class RolInline(admin.TabularInline): #agregar esto permite que no aparezca el rol en admin si no que en el usuario aparezcan 3 espacios para agregar roles a ese usuario
    model = Rol
    extra = 3 #3 roles, proporciona 3 roles para los usuarios relacion 1 a muchos, 1 usuario, muchos roles, es ideal para 1 usuario muchas materias

class UsuarioAdmin(admin.ModelAdmin):
    fields = ['uid', 'password','fecha_creacion']
    inlines = [RolInline]
    list_display = ('uid', 'fecha_creacion', 'was_published_recently') #si o si usar list_display esto muestra los objetos junto a su valor
    list_filter = ['fecha_creacion'] #esto crea una barra de filtro para fecha
    search_fields = ['uid'] #agregar busqueda de uid

class DirectivoAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Nombre completo', {'fields': [
            'nombre',
            'apellido'
        ]}),
        (None,              {'fields': [
            'dni',
            'mail',
            'id_usuario'
        ]}),
    ]

# esto permite agregar objetos a mano pero no es lo ideal
admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Directivo, DirectivoAdmin)
admin.site.register(Permiso)
admin.site.register(Curso)
admin.site.register(Alumno)
admin.site.register(Materia)
admin.site.register(MateriaAlumno)
# ahora en admin se pueden ver todos los roles y permisos creados