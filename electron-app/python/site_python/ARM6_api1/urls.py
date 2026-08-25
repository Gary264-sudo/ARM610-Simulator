# Este urls ha sido creado en el ARM6_api1
from django.urls import include, path
from rest_framework import routers
from . import views

# ¿Que es un views?

# ¿Que es un Router class?
# Router class combina recursos en views y urls de manera que puedan ser manejados automaticamente
router = routers.DefaultRouter()

# Este es un nuevo url:
#  - '' significa que es el root URL
#  - views.index significa que ejecutara la funcion index del script views del API
#  - name significa el nombre del URL (se recomienda el mismo nombre que el URL)
router.register(r'ARM6_api1', views.index, basename="ARM6_api1")

# Por ejemplo:
# '/MMU' significa que es un URL especifico
# path('/MMU', views.index, name='index');


# Crearemos una lista de URLs
urlpatterns = [
    path('', include(router.urls)),
]
