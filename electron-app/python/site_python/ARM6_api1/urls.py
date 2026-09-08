# Este urls ha sido creado en el ARM6_api1
# Se encargara de realizar el URL Mapping de ARM6_api1

from django.urls import include, path
from . import views

# ¿Que es un views?

# Crearemos una lista de URLs
urlpatterns = [
    # Este es un nuevo url:
    #  - '' significa que es el root URL
    #  - views.index significa que ejecutara la funcion index del script views del API
    #  - name significa el nombre del URL (se recomienda el mismo nombre que el URL)
    path('', views.index, name='index'),
    path('PCvalue/', views.PCvalue, name='PC'),
    path('MP_ram/', views.Loader, name='MP_ram'),

    # Por ejemplo:
    # '/MMU' significa que es un URL especifico
    # path('/MMU', views.index, name='index');
]
