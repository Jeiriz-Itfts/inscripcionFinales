from rest_framework.serializers import ModelSerializer
from .models import *

class UsuarioSeriazer (ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'

class MateriaAlumnoSeriazer (ModelSerializer):
    class Meta:
        model = MateriaAlumno
        fields = '__all__'