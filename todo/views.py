from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from .forms import TodoForm
from .models import Todolist
from django.utils import timezone
from django.contrib.auth.decorators import login_required


def home(request):
    return render (request, 'todo/home.html')


def signupuser(request):
    if request.method == 'GET':
        return render(request, 'todo/signupuser.html', {'form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('currenttodos')
            except IntegrityError:
                return render(request, 'todo/signupuser.html', {'form': UserCreationForm(), 'error': 'Такой пользователь уже существует. Задайте новое имя.'})
        else:
            return render(request, 'todo/signupuser.html', {'form': UserCreationForm(), 'error': 'Пароль не совпадает'})

def loginuser(request):
    if request.method == 'GET':
        return render(request, 'todo/loginuser.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'todo/loginuser.html', {'form': AuthenticationForm(), 'error': 'Пользователь и пароль не найдены'})
        else:
            login(request, user)
            return redirect('currenttodos')

@login_required()
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

@login_required()
def createtodo(request):
    if request.method == 'GET':
        return render(request, 'todo/createtodo.html', {'form': TodoForm()})
    else:
        try:
            form = TodoForm(request.POST)
            if form.is_valid():
                new_to_do = form.save(commit=False)
                new_to_do.user = request.user
                new_to_do.save()
                return redirect('currenttodos')
        except ValueError:
            return render(request, 'todo/createtodo.html', {'form': TodoForm(), 'error': 'Были переданы неверные данные. Попробуйте снова.'})

@login_required()
def currenttodos(request):
    todos = Todolist.objects.filter(user=request.user, date_completed__isnull=True)
    return render(request, 'todo/currenttodos.html', {'todos': todos})

@login_required()
def completedtodos(request):
    todos = Todolist.objects.filter(user=request.user, date_completed__isnull=False).order_by('-date_completed')
    return render(request, 'todo/completedtodos.html', {'todos': todos})

@login_required()
def viewtodo(request, todo_pk):
    todo = get_object_or_404(Todolist, pk=todo_pk, user=request.user)
    if request.method == 'GET':
        form = TodoForm(instance=todo)
        return render(request, 'todo/viewtodo.html', {'todo': todo, 'form': form})
    else:
        try:
            form = TodoForm(request.POST, instance=todo)
            form.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todo/viewtodo.html', {'todo': todo, 'form': form, 'error': 'Неправильно введеные данные'})

@login_required()
def completetodo(request, todo_pk):
    todo = get_object_or_404(Todolist, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.date_completed = timezone.now()
        todo.save()
        return redirect('currenttodos')

@login_required()
def confirm_deletetodo(request, todo_pk):
    todo = get_object_or_404(Todolist, pk=todo_pk, user=request.user)
    return redirect('deletetodo')

@login_required()
def deletetodo(request, todo_pk):
    todo = get_object_or_404(Todolist, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.date_deleted = timezone.now()
        todo.delete()
        return redirect('currenttodos')

@login_required()
def deletedtodos(request):
    todos = Todolist.objects.filter(user=request.user, date_deleted__isnull=False).order_by('-date_deleted')
    return render(request, 'todo/deletedtodos.html', {'todos': todos})



