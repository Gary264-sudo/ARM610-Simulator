Semana 1: Setting up the environment
Semana 2: Creacion del ensamblador
 - Conocimiento del funcionamiento de un ensamblador (absoluto)
Semana 3: 
 - Construccion del ensamblador

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

npm install axios

python manage.py runserver (Inicializar el servidor de Django)

De manera de prevenir el error de Content Security Policy (https://www.electronjs.org/docs/latest/tutorial/security#7-define-a-content-security-policy)
<meta
      http-equiv="Content-Security-Policy"
      content="connect-src 'self' http://127.0.0.1:8000 'unsafe-eval';
        default-src 'self'; 
        script-src 'self';
        style-src 'self' 'unsafe-inline';
        img-src 'self' data:"
    />

De manera de prevenir el error de XMLHttpRequest
"Access to XMLHttpRequest at 'http://127.0.0.1:8000/PCvalue/?input=10' from origin 'http://localhost:5173' has been blocked by CORS policy: No 'Access-Control-Allow-Origin' header is present on the requested resource."

const UpsertKeyValue = (obj : any, keyToChange : string, value : string[]) => {
  const keyToChangeLower = keyToChange.toLowerCase();
  for (const key of Object.keys(obj)) {
    if(key.toLowerCase() === keyToChangeLower) {
      obj[key] = value;
      return;
    }
  }
  obj[keyToChange] = value;
}

mainWindow.webContents.session.webRequest.onBeforeSendHeaders((details, callback) => {
      const { requestHeaders } = details;
      UpsertKeyValue(requestHeaders, 'Access-Control-Allow-Origin', ['*']);
      callback({ requestHeaders });
    },
  );

  mainWindow.webContents.session.webRequest.onHeadersReceived((details, callback) => {
    const { responseHeaders } = details;
    UpsertKeyValue(responseHeaders, 'Access-Control-Allow-Origin', ['*']);
    UpsertKeyValue(responseHeaders, 'Access-Control-Allow-Origin', ['*']);
    callback({
      responseHeaders,
    });
  });

4. Comenzar a codificar python y React
La manera en como se envian los datos mediante las APIs de Django hacia la aplicacion de Electron es de la siguiente manera:
    1. Publicar los datos en Django
    2. Obtener los datos mediante Axios
    3. Enviarlos a la aplicacion

5. Acerca del ensamblador
Usualmente el ensamblador tiene dos identification bits de manera de detectar cuatro tipos especificos por instruccion:
 - 00: absolute machine instruction
 - 01: relative machine instruction
 - 10: machine instruction that requires special relocation.
 - 11: a loader directive
En este caso, en lugar de realizarse por instruccion, se ha realizado por operando.

