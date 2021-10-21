from django.db import models

# Create your models here.
# Tantos modelos como tablas
class Rol(models.Model):
    descripcion = models.CharField(max_length=200)

class Permiso(models.Model):
    id_rol = models.ForeignKey(Rol, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=200)
    descripcion = models.CharField(max_length=200)