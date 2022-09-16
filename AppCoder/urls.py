from django.urls import path
from AppCoder.views import *        # con * importa todas las clases que esten en views


urlpatterns = [
    path('', inicio),               # si se deja en blaco la pagina despues del path, redirige a la que este despues de la coma, en este caso a inicio
    path('cursos/', cursos),
    path('entregables/', entregables),
    path('estudiantes/', estudiantes),
    path('profesores/', profesores),
    path('home/', home),
    path('api_estudiantes/', api_estudiantes),
    path('buscar_estudiante/', buscar_estudiante),
    
]