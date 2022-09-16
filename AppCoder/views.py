from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse
from AppCoder.models import Estudiante
from AppCoder.forms import form_estudiantes

def inicio(request):
    return render(request, "inicio.html")

def cursos(request):
    return render(request, "cursos.html")

def profesores(request):  
    return render(request, "profesores.html")

def estudiantes(request):
    if request.method == "POST":
        estudiante = Estudiante(nombre=request.POST['nombre'], apellido=request.POST['apellido'], email=request.POST['email'])
        estudiante.save()
        return render(request, "home.html")
    return render(request, "estudiantes.html")

def entregables(request):
    return render(request, "entregables.html")

def home(request):
    return render(request, "home.html")

def api_estudiantes(request):
    if request.method == "POST":
        formulario = form_estudiantes(request.POST)
        if formulario.is_valid():
            informacion = formulario.cleaned_data
            estudiante=Estudiante(nombre=informacion['nombre'], apellido=informacion['apellido'], email=informacion['email'])
            estudiante.save()
            return render(request, "api_estudiantes.html")        
       
    else:
        formulario = form_estudiantes()
    return render(request, "api_estudiantes.html", {"formulario": formulario})


def buscar_estudiante(request):
    if request.GET["email"]:
        email = request.GET["email"]
        estudiantes = Estudiante.objects.filter(email__icontains = email) 
        return render(request, "estudiantes.html", {"estudiantes": estudiantes})
    else:
        respuesta = "No enviaste datos"
    return HttpResponse(respuesta)
