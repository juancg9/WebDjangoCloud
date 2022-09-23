from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.http import HttpResponse
from AppCoder.models import Estudiante
from AppCoder.forms import form_estudiantes, UserRegisterForm
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm      #formularios propios de django para autenticacion de usuarios
from django.contrib.auth import login, logout, authenticate         #formularios propios de django para autenticacion de usuarios
from django.contrib.auth.decorators import login_required              


def inicio(request):
    return render(request, "inicio.html")

def cursos(request):
    return render(request, "cursos.html")

def profesores(request):  
    return render(request, "profesores.html")

@login_required                                         # solo permite ingresar cuando se ha registrado el usuario
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


def create_estudiantes(request):
    if request.method == 'POST':
        estudiante = Estudiante(nombre = request.POST['nombre'], apellido = request.POST['apellido'], email = request.POST['email'])
        estudiante.save()     
        estudiantes = Estudiante.objects.all()   # trae toda la info 
        return render(request, "estudiantesCRUD/read_estudiantes.html", {"estudiantes": estudiantes}) 

    return render(request, "estudiantesCRUD/create_estudiantes.html")

def read_estudiantes(request):
    estudiantes = Estudiante.objects.all()   # trae toda la info 
    return render(request, "estudiantesCRUD/read_estudiantes.html", {"estudiantes": estudiantes})




def update_estudiantes(request, estudiante_id):
    estudiante = Estudiante.objects.get(id = estudiante_id)

    if request.method == 'POST':
        formulario = form_estudiantes(request.POST)

        if formulario.is_valid():
            informacion = formulario.cleaned_data
            estudiante.nombre = informacion['nombre']
            estudiante.apellido = informacion['apellido']
            estudiante.email = informacion['email']
            estudiante.save()
            estudiantes = Estudiante.objects.all() #Trae toda la info
            return render(request, "estudiantesCRUD/read_estudiantes.html", {"estudiantes": estudiantes})
    else:
        formulario = form_estudiantes(initial={'nombre': estudiante.nombre, 'apellido': estudiante.apellido, 'email': estudiante.email})
    return render(request,"estudiantesCRUD/update_estudiantes.html", {"formulario": formulario})



def delete_estudiantes(request, estudiante_id):
    estudiante = Estudiante.objects.get(id = estudiante_id)      # a la variable estudiante del momdelo Estudiante se le asigna (get) la variable email que viene por referencia
    estudiante.delete()
    estudiantes = Estudiante.objects.all()
    return render(request, "estudiantesCRUD/read_estudiantes.html", {"estudiantes": estudiantes})

def login_request(request):
    if  request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.cleaned_data.get('username')
            pwd = form.cleaned_data.get('password')
            user = authenticate(username = user, password = pwd)

            if user is not None:
                login(request, user)
                return render(request, "home.html")
            else:
                return render(request, "login.html", {'form':form})
        else:
            return render(request, "login.html", {'form':form})
    form = AuthenticationForm()
    return render(request, 'login.html', {'form':form})

def registro(request):
    if request.method == 'POST':
        #form = UserCreationForm(request.POST)
        form = UserRegisterForm(request.POST)
        if form.is_valid():
           # username = form.cleaned_data["username"]
            form.save()
            return render(request, "inicio.html")
    #form = UserCreationForm()
    form = UserRegisterForm()
    return render(request, 'registro.html', {'form':form})
