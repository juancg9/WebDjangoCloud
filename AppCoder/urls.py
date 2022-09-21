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
    path('create_estudiantes/', create_estudiantes),
    path('read_estudiantes/', read_estudiantes),
    path('update_estudiantes/<estudiante_id>', update_estudiantes),
    path('delete_estudiantes/<estudiante_id>', delete_estudiantes),
    
]