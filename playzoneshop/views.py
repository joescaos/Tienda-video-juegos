from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import RegisterForm
from games.models import Game

def index(request):
    games = Game.objects.all()
    return render(request, 'index.html', {
        'games': games,

    })

def login_view(request):

    if request.user.is_authenticated:
        return redirect('index')
        
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, "Bienvenido {}".format(user.username))
            return redirect('index')
        else:
            messages.error(request, "Usuario o contraseña no válidos")

    return render(request, 'users/login.html', {
        
    })

def logout_view(request):
    logout(request)
    messages.success(request, "Sesión cerrada exitosamente")
    return redirect('index')

def registrar(request):

    if request.user.is_authenticated:
        return redirect('index')
    form = RegisterForm(request.POST or None) 
    if request.method == 'POST' and form.is_valid():
        '''username = form.cleaned_data.get('username')
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')'''
        # user = User.objects.create_user(username, email, password)
        user = form.save()
        if user:
            login(request, user)
            messages.success(request, "Usuario creado correctamente")
            return redirect('index')


    return render(request, 'users/newuser.html', {
        'form': form,
    })