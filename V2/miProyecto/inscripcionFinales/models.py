
# Create your models here.
from django.db import models
from django.conf import settings



# Create your models here.
# Tantos modelos como tablas


class Curso(models.Model):
    descripcion = models.CharField(max_length=200,  unique=True)


class Materia(models.Model):
    # si debes crear registros, se pone la instancia de la foregihn key que usa, como curso
    id_curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=200,  unique=True)

class MateriaAlumno(models.Model):
    id_materia = models.ForeignKey(Materia, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    fecha_inscripcion = models.DateTimeField('Fecha inscripción')
    
