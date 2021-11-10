from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from .models import Usuario
from django.utils import timezone
from django.urls import reverse


def index(request):
    return render(request, 'inscripcionFinales/index.html')


def reset(request):
    return render(request, 'inscripcionFinales/reset.html')

# def vote(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     try:
#         selected_choice = question.choice_set.get(pk=request.POST['choice'])
#     except (KeyError, Choice.DoesNotExist):
#         # Redisplay the question voting form.
#         return render(request, 'polls/detail.html', {
#             'question': question,
#             'error_message': "You didn't select a choice.",
#         })
#     else:
#         selected_choice.votes += 1
#         selected_choice.save()
#         # Always return an HttpResponseRedirect after successfully dealing
#         # with POST data. This prevents data from being posted twice if a
#         # user hits the Back button.
# Después de incrementar el conteo de la elección, el código retorna una HttpResponseRedirect en lugar de una HttpResponse normal HttpResponseRedirect toma un único argumento: La URL a la que el usuario será redirigido (vea el siguiente aspecto de cómo construimos la URL en este caso).
#
# As the Python comment above points out, you should always return an HttpResponseRedirect after successfully dealing with POST data. This tip isn’t specific to Django; it’s good Web development practice in general.
#
# Estamos utilizando la función reverse() en el constructor HttpResponseRedirect en este ejemplo. Esta función ayuda a evitar tener que codificar una URL en la función de vista. Se proporciona el nombre de la vista a la que queremos pasar el control y la parte de la variable del patrón de URL que señala esa vista. En este caso, utilizando la URLconf que configuramos en el Tutorial 3, esta llamada reverse() retornará una cadena como

def probar_excepcion(request,usuario_id):
    usuarios = get_object_or_404(Usuario, pk=usuario_id) #toma un modelo y numero de arg
    context = {'usuarios': usuarios} #diccionario para pasarle al template
    return render(request, 'inscripcionFinales/usersPlantilla.html',context)


def users_plantilla(request):
    try:
        usuarios = Usuario.objects.all() #pk=algo_id
        context = {'usuarios': usuarios} #diccionario para pasarle al template
    except Usuario.DoesNotExist:
        raise Http404("No existe el usuario")
    return render(request, 'inscripcionFinales/usersPlantilla.html',context) #el render toma el objeto, nombre plantilla, y diccionario, retorna un Httpresponse

# path('usuario/', views.insertarUsr, name='insertarUsr'),
def insertar_usr(request):
    usuario = Usuario(uid="carlos", password="carlitos", fecha_creacion=timezone.now())
    usuario.save()
    return HttpResponse("Usuario creado: %s " % usuario.uid)

# /usuarios
def get_usrs(request):
    usrsLista = Usuario.objects.all()
    # usrsLista = Usuario.objects.filter(id=2)
    usrsListaFinal = ', '.join([usuario.uid for usuario in usrsLista])
    return HttpResponse(usrsListaFinal)

# Forma 1
# Django permite muchas cosas, usar muchas vistas y devolver muchas cosas pero siempre se debe
# retornar un httpresponse o http404
def get_id(request, usuario_id):
    response = "Estas buscando el usuario con uid %s."
    return HttpResponse(response % usuario_id)

# Forma  2
# def getUsr(request, usuario_id):
#    return HttpResponse("Estas buscando el usuario con id %s." % usuario_id)
