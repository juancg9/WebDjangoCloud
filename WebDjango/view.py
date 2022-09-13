from django.http import HttpResponse
from django.template import loader      # herrmienta de Django
from AppCoder.models import Curso

def home(self, name):
    return HttpResponse(f' Hola, soy {name}')

def homePage(self):
    lista = [1,2,3,4,5,6,7,8,9]
    data = {'nombre':'Juan',        # definicion del Diccionario
    'apellido':'Gonzalez',
    'lista':lista}          # se puede hacer salto de linea despues de la , en el Diccionario
    planilla = loader.get_template('home.html')  # ahorra escribir el camino porque loader lo va a tener y se configura en el loader en otro lado
    documento = planilla.render(data)       # la opcion render es para dibujar o mostrar algo y se muestra lo q este en parentesis
    return HttpResponse(documento)

def cursos(self):
    #planilla = loader.get_template('cursos.html')
    curso = Curso(nombre='XU/XI', camada='12345')
    curso.save()

    documento = f'Curso: {curso.nombre} camada: {curso.camada}'
    return HttpResponse(documento)