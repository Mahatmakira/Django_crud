from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse
from .forms import TaskForm
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required

# Create your views here.

#Pagina principal
def home(request):
    return render(request, 'home.html')

#Registro de usuario
def signup(request):

    if request.method == "GET":
        print("enviando")
        return render(request, "signup.html", {
            "form": UserCreationForm
        })
    else:
        if request.POST["password1"] == "":
            return render(request, "signup.html", {
                'form': UserCreationForm,
                "error": "Ingrese una contraseña valida"
            })
        else:
            if request.POST["password1"] == request.POST["password2"]:
                # Se registra el usuario
                try:
                    user = User.objects.create_user(username=request.POST["username"],
                                                    password=request.POST["password1"])
                    user.save()
                    login(request, user)
                    return redirect("task")

                except IntegrityError:
                    return render(request, "signup.html", {
                        'form': UserCreationForm,
                        "error": "Usuario ya existe"
                    })
            else:
                return render(request, "signup.html", {
                    'form': UserCreationForm,
                    "error": "Contraseñas no coinciden"
                })

#Salir de sección
@login_required
def signout(request):
    logout(request)
    return redirect("home")

#Ingreso de usuario
def signin(request):
    if request.method == "GET":
        # print("enviando")
        return render(request, "signin.html", {
            "form": AuthenticationForm
        })
    else:
        user = authenticate(
            request, username=request.POST["username"],
            password=request.POST["password"]
        )
        if user is None:
            return render(request, "signin.html", {
                'form': AuthenticationForm,
                "error": "El usuario o contraseña son incorrectos"
            })
        else:
            login(request,user)
            return redirect("task")
        
#Ventana con tareas pendientes
@login_required
def task(request):
    tasks = Task.objects.filter(user=request.user, date_completed__isnull=True)
    return render(request, "task.html", {'tasks': tasks})

#Ventana con tareas finalizadas
@login_required
def task_ending(request):
    tasks = Task.objects.filter(user=request.user, date_completed__isnull=False).order_by("-date_completed")
    return render(request, "task.html", {'tasks': tasks})

#Creación de tareas
@login_required
def create_task(request):
    # Se usa metodo GET cuando se esta entrando al formulario
    if request.method == "GET":
        return render(request, "create_task.html", {"form": TaskForm()})
    else:
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save() 
            return redirect("task")
        except ValueError:
            return render(request, "create_task", {
                'form': TaskForm,
                "error": "Los datos ingresados son invalidos"
            })
#Detalle de la tarea
@login_required
def task_detail(request,task_id):
    # Se usa metodo GET cuando se esta entrando al formulario
    if request.method == "GET":
        task = get_object_or_404(Task, pk=task_id)
        form = TaskForm(instance=task)
        return render(request, "task_detail.html", {
            "task": task , "form": form
        })
    else:
        try:
            ##Se usan las isguientes lineas de código para modificar 
            task = get_object_or_404(Task, pk=task_id, user=request.user)
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect('task')
        except ValueError:
            return render(request, "task_detail.html", {
            "task": task , "form": form, "error": "Error al modificar"
            })

#Acción ejecutada por el boton que asigna fecha de completado de tarea
@login_required
def task_complete(request, task_id): 
    task = get_object_or_404(Task, pk=task_id,user=request.user)
    if request.method == "POST":
        task.date_completed = timezone.now()
        task.save()
        return redirect("task")
    
#Acción ejecutada por el bóton que borra la tarea
@login_required    
def task_delete(request, task_id): 
    task = get_object_or_404(Task, pk=task_id,user=request.user)
    if request.method == "POST":
        task.delete()
        return redirect("task")