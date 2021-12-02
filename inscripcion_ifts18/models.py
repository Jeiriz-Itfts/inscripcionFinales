from django.db import models
from django.utils import timezone
import datetime
from django.contrib import admin


# Create your models here.
# Tantos modelos como tablas


class Usuario(models.Model):
    uid = models.CharField(max_length=200, unique=True)
    password = models.CharField(max_length=200)
    fecha_creacion = models.DateTimeField('Fecha creación')
    mail = models.EmailField(max_length=254, unique=True)

    """ este metodo se agrega para que cuando llame al objeto, me devuelva info util """
    def __str__(self):
        return self.uid


class Rol(models.Model):
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=200,  unique=True)
    def __str__(self):
        return self.descripcion


class Permiso(models.Model):
    id_rol = models.ForeignKey(Rol, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=200,  unique=True)
    descripcion = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre

class Directivo(models.Model):
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=200)
    apellido = models.CharField(max_length=200)
    dni = models.CharField(max_length=200,  unique=True)

    def __str__(self):
        return self.nombre + " " + self.apellido

class Administradores(models.Model):
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=200)
    apellido = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre + " " + self.apellido

class Curso(models.Model):
    descripcion = models.CharField(max_length=200,  unique=True)

    def __str__(self):
        return self.descripcion

class Alumno(models.Model):
    id_curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=200)
    apellido = models.CharField(max_length=200)
    legajo = models.CharField(max_length=200, unique=True)
    dni = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.nombre + " " + self.apellido

class Materia(models.Model):
    id_curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=200,  unique=True)

    def __str__(self):
        return self.descripcion

class MateriaAlumno(models.Model):
    id_materia = models.ForeignKey(Materia, on_delete=models.CASCADE,  unique=True)
    id_alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    fecha_inscripcion = models.DateTimeField('Fecha inscripción')
    
    def __str__(self):
        return self.fecha_inscripcion