from django.db import models
from django.utils import timezone
import datetime
from django.contrib import admin
from django.conf import settings


# Create your models here.
# Tantos modelos como tablas


class Curso(models.Model):
    descripcion = models.CharField(max_length=200,  unique=True)


class Materia(models.Model):
    id_curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=200,  unique=True)

class MateriaAlumno(models.Model):
    id_materia = models.OneToOneField('Materia', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    fecha_inscripcion = models.DateTimeField('Fecha inscripción')
    
