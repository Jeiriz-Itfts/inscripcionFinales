from django.db import models
from django.utils import timezone
import datetime
from django.contrib import admin


# Create your models here.
# Tantos modelos como tablas


class Usuario(models.Model):
    uid = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    fecha_creacion = models.DateTimeField('Fecha creación')
    mail = models.EmailField(max_length=254)


class Rol(models.Model):
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=200)


class Permiso(models.Model):
    id_rol = models.ForeignKey(Rol, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=200)
    descripcion = models.CharField(max_length=200)


class Directivo(models.Model):
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=200)
    apellido = models.CharField(max_length=200)
    dni = models.CharField(max_length=200)

class Administradores(models.Model):
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=200)
    apellido = models.CharField(max_length=200)


class Curso(models.Model):
    descripcion = models.CharField(max_length=200)


class Alumno(models.Model):
    id_curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=200)
    apellido = models.CharField(max_length=200)
    legajo = models.CharField(max_length=200)
    dni = models.CharField(max_length=200)


class Materia(models.Model):
    id_curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=200)


class MateriaAlumno(models.Model):
    id_materia = models.ForeignKey(Materia, on_delete=models.CASCADE)
    id_alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    fecha_inscripcion = models.DateTimeField('Fecha inscripción')
