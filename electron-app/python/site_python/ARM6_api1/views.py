from django.shortcuts import render
from django.http import HttpResponse

from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

# Create your views here.
# Aqui se crearan las funciones que se desplegaran en una determinada URL

class index(viewsets.ViewSet):

    

    @action(methods=['GET'], detail = False, name = 'Get value from Input')

    def IR(self, request):
        input = request.GET['input']
        return Response(status=status.HTTP_200_OK, data=1)
