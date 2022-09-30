from urllib import request
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.http import HttpResponse
from AppCoder.models import Estudiante, Curso, Avatar
from AppCoder.forms import form_estudiantes, UserRegisterForm, UserEditForm, ChangePasswordForm, AvatarFormulario

from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm     #formularios propios de django para autenticacion de usuarios
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash         #formularios propios de django para autenticacion de usuarios
from django.contrib.auth.decorators import login_required      
from django.contrib.auth.models import User
       


def inicio(request):
    return render(request, "inicio.html")

def cursos(request):
    return render(request, "cursos.html")

def profesores(request):  
    return render(request, "profesores.html")

# si se intenta ingresar a una página que requiera autenticacion como este caso, arroja error.
# Para evitar el error se coloca en WebDjango en Setting la sentencia para redirigir a Login
@login_required                                         # solo permite ingresar cuando se ha registrado el usuario
def estudiantes(request):
    if request.method == "POST":
        estudiante = Estudiante(nombre=request.POST['nombre'], apellido=request.POST['apellido'], email=request.POST['email'])
        estudiante.save()
        avatar = Avatar.objects.filter(user = request.user.id)
        try:
            avatar = avatar[0].image.url
        except:
            avatar = None
        return render(request, 'home.html', {'avatar': avatar})
    return render(request, "estudiantes.html")

def entregables(request):
    return render(request, "entregables.html")


def home(request):
    avatar = Avatar.objects.filter(user = request.user.id)
    try:
        avatar = avatar[0].image.url
    except:
        avatar = None
    return render(request, "home.html", {'avatar':avatar})

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
    if request.method == 'POST':
        form = AuthenticationForm(request, data = request.POST)
        if form.is_valid():
            user = form.cleaned_data.get('username')
            pwd = form.cleaned_data.get('password')

            user = authenticate(username = user, password = pwd)

            if user is not None:
                login(request, user)
                avatar = Avatar.objects.filter(user = request.user.id)
                try:
                    avatar = avatar[0].image.url
                except:
                    avatar = None
                return render(request, 'home.html', {'avatar': avatar})
            else:
                return render(request, "login.html", {'form':form})
        else:
            return render(request, "login.html", {'form':form})
    form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

# def registro(request):
#     if request.method == 'POST':
#         #form = UserCreationForm(request.POST)
#         form = UserRegisterForm(request.POST)
#         if form.is_valid():
#            # username = form.cleaned_data["username"]
#             form.save()
#             return render(request, "inicio.html")
#     #form = UserCreationForm()
#     form = UserRegisterForm()
#     return render(request, 'registro.html', {'form':form})


def registro(request):
    form = UserRegisterForm(request.POST)
    if request.method == 'POST':
        # user = UserCreationForm(request.POST)
        # print(form) 
        if form.is_valid():
            # username = form.cleaned_data["username"]
            form.save()
            return redirect("/AppCoder/login")
        else:
            return render(request, "registro.html", {'form': form})
    # form = UserRegisterForm()

    form = UserRegisterForm()
    return render(request, "registro.html", {'form': form})


@login_required
def editarPerfil(request):
    usuario = request.user
    user_basic_info = User.objects.get(id = usuario.id)
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance = usuario)
        if  form.is_valid():
            # Datos que se desean actualizar
            user_basic_info.username = form.cleaned_data.get('username')
            user_basic_info.email = form.cleaned_data.get('email')
            user_basic_info.first_name = form.cleaned_data.get('first_name')
            user_basic_info.last_name = form.cleaned_data.get('last_name')
            user_basic_info.save()
            avatar = Avatar.objects.filter(user = request.user.id)
            try:
                avatar = avatar[0].image.url
            except:
                avatar = None
            return render(request, "home.html", {'avatar': avatar})
        else:
            avatar = Avatar.objects.filter(user = request.user.id)
            try:
                avatar = avatar[0].image.url
            except:
                avatar = None
            return render(request, "home.html", {'form':form, 'avatar': avatar})
            #return render(request, 'home.html', {'form':form})  # retorna el formulario para ver que es lo que falla
    else:
      #  form = UserEditForm(initial={'email': usuario.email, 'username': usuario.username, 'first_name': usuario.first_name, 'last_name': usuario.last_name})
        form = UserEditForm(initial={'email': usuario.email, 'username': usuario.username, 'first_name': usuario.first_name, 'last_name': usuario.last_name })
    return render(request, 'editarPerfil.html', {'form': form, 'usuario': usuario})


@login_required
def changepass(request):
    usuario = request.user
    if request.method == 'POST':
        # form = PasswordChangeForm(data = request.POST, user = usuario)     #este formulario es el de defecto de Django
        form = ChangePasswordForm(data = request.POST, user = request.user)  # FORMULARIO CREADO EN FORMS
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            avatar = Avatar.objects.filter(user = request.user.id)
            try:
                avatar = avatar[0].image.url
            except:
                avatar = None
            return render(request, "home.html", {'avatar': avatar})
    else:
        # form = PasswordChangeForm(request.user)                       #este formulario es el de defecto de Django
        form = ChangePasswordForm(user = request.user)
    return render(request, 'changepass.html', {'form':form, 'usuario':usuario}) 


# @login_required
# def perflView(request):
#     usuario = request.user
#     user_basic_info = User.objects.get(id = usuario.id)
#     print(usuario)
#     return render(request, 'perfil.html', {'form':user_basic_info})
    
# VERSION MINIMALSTA DE LA ANTERIOR
@login_required
def perfilView(request):
    avatar = Avatar.objects.filter(user = request.user.id)
    try:
        avatar = avatar[0].image.url
    except:
        avatar = None
    return render(request, "perfil.html", {'avatar': avatar})
    
    
# def AgregarAvatar(request):
#     if request.method == 'POST':
#         form = AvatarFormulario(request.POST, request.FILES)
#         if form.is_valid():
#             user = User.objects.get(username = request.user)
#             avatar = Avatar(user = user, image = form.cleaned_data['avatar'], id = request.user.id)
#             avatar.save()
#             avatar = Avatar.objects.filter(user = request.user.id)
#             try:
#                 avatar = avatar[0].image.url
#             except:
#                 avatar = None
#             return render(request, "home.html", {'avatar': avatar})
#     else:
#         try:
#             avatar = Avatar.objects.filter(user = request.user.id)
#             form = AvatarFormulario()
#         except:
#             form = AvatarFormulario()
#     return render(request, "AgregarAvatar.html", {'fomr': form})



@login_required
def AgregarAvatar(request):
    if request.method == 'POST':
        form = AvatarFormulario(request.POST, request.FILES)
        print(form)
        print(form.is_valid())
        if form.is_valid():
            user = User.objects.get(username = request.user)
            avatar = Avatar(user = user, image = form.cleaned_data['avatar'], id = request.user.id)
            avatar.save()
            avatar = Avatar.objects.filter(user = request.user.id)
            try:
                avatar = avatar[0].image.url
            except:
                avatar = None           
            return render(request, 'home.html', {'avatar': avatar})
    else:
        try:
            avatar = Avatar.objects.filter(user = request.user.id)
            form = AvatarFormulario()
        except:
            form = AvatarFormulario()
    return render(request, 'AgregarAvatar.html', {'form': form})


# def AgregarAvatar(request):
#     if request.method == 'POST':
#         form = AvatarFormulario(request.POST, request.FILE)
#         if form.is_valid():
#             user = User.objects.get(username = request.user)
#             avatar = Avatar(user = user, image = form.cleaned_data['avatar'], id = request.user.id)
#             avatar.save()
#             avatar = Avatar.objects.filter(user = request.user.id)
#             return render(request, 'home.html', {'avatar': avatar[0].image.url})
#     else:
#         try:
#             avatar = Avatar.objects.filter(user = request.user.id)
#             form = AvatarFormulario()
#         except:
#             form = AvatarFormulario()
#     return render(request, 'AgregarAvatar.html', {'form': form})
