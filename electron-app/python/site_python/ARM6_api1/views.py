from django.shortcuts import render
from django.http import HttpResponse

from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

# Create your views here.
# Aqui se crearan las funciones que se desplegaran en una determinada URL

reloj = {0, 0, 0, 0, 0, 0, 0, 0}

class index(viewsets.ViewSet):
    @action(methods=['GET'], detail = False, name = 'Get value from Input')

    def get_val_from(self, request):
        input = request.GET['input2']
        return Response(status=status.HTTP_200_OK,
                        data = input)

    def PCvalue(self, request):
        # El PC tiene un tamaño de 12 bits
        # Esta sincronizado por el generador de pulsos de reloj
        
        count = 0

        # Si el reloj tuviese un segundo pulso de reloj, se realiza el incremento del PC
        # if(reloj[2] == 1):
        #     count = count + 1
        
        input = request.GET['input']
        return Response(status=status.HTTP_200_OK, data=count)

    def IR(self, request):
        input = request.GET['input3']
        return Response(status=status.HTTP_200_OK, data=1)
