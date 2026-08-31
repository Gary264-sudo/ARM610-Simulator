from django.shortcuts import render
from django.http import HttpResponse

from rest_framework import status
from rest_framework.decorators import api_view, action
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

# Create your views here.
# Aqui se crearan las funciones que se desplegaran en una determinada URL

# Static template: Es una pagina que no tiene cambios
# Dynamic template: Es una pagina que tiene cambios debido a una funcion en particular

# Publicar los datos en Django -> obtener los datos mediante Axios -> Enviarlos a la aplicacion

reloj = {0, 0, 0, 0, 0, 0, 0, 0}

@api_view(('GET',))
@action(methods=['GET'], detail = False, name='Get value from input')
def index(request):
    pass

def get_val_from(self, request):
    input = request.GET['input2']
    return HttpResponse(data = input)

@api_view(('GET',))
@action(methods=['GET'], detail = False, name='Get value from input')
def PCvalue(request):
    # El PC tiene un tamaño de 12 bits
    # Esta sincronizado por el generador de pulsos de reloj

    input = request.GET['input']

    # Si el reloj tuviese un segundo pulso de reloj, se realiza el incremento del PC
    # if(reloj[2] == 1):
    #     count = count + 1
    
    return Response(status=status.HTTP_200_OK, data = input)

def IR(self, request):
    input = request.GET['input3']
    return Response(status=status.HTTP_200_OK, data=1)

# class index(viewsets.ViewSet):

