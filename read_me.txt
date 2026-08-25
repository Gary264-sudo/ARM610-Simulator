(https://ivanyu2021.hashnode.dev/electron-django-desktop-app-integrate-javascript-and-python)
1. Create a Electron project

2. Setting the virtual environment in a Python folder inside the electron-app
mkdir Python
py -m pip install --user virtualenv
py -m venv virtualenv
.\virtualenv\Scripts\activate (Activar el virtual environment)

pip install django
pip install django djangorestframework
npm install axios (axios se aplicara en react) (https://www.freecodecamp.org/espanol/news/como-usar-axios-con-react/)

django-admin startproject site_python

(https://stackoverflow.com/questions/67586182/how-to-resolve-import-django-contrib-could-not-be-resolved-from-source-in-vs)
(https://stackoverflow.com/questions/511291/django-installed-apps-location)
crtl + shift + p
 -> Python: Select interpreter
  ->Enter interpreter path
   -> Find
    -> Scripts/python.exe

add 'rest_framework' in INSTALLED_APPS in settings.py from site_python (django project)

Crear un const initiateOrderDjango que inicialice django cuando se inicie Electron

3. Crear las APIs

python manage.py startapp API

add path('', include(API.urls)), in \site_python\site_python\urls.py



4. 


