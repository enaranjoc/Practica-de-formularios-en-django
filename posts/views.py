from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate 
from .models import Post
from .forms import PostForm



# Create your views here.
def index(request):
    return render(request,'index.html', {'posts': Post.objects.all()})

def crearPost(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            # form.save()
            post = form.save(commit=False) #Con el parametro commit permite que los datos se guarden en la variable pos y no directamente en la bd
            post.autor = request.user
            post.save()
            return redirect('index')
    else:
        form = PostForm()
        return render(request, 'creacion.html', {'form': form})

'''Registrar usuario'''
'''Para poder utilizar el formulario de registro de usuario de django se debe de imortar
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate 
Y lugo se debe de crear una carpeta con el nombre de "registration" 
ya que en dicha carpeta django buscara los html com los formularios.

Adema en el archivo settings.py se debe de colocar  la siguiente linea de codigo
LOGIN_REDIRECT_URL = 'index'
que indica la url a la que se debe de redirigir una ves se realize el formulario de 
inicio de secion.'''

def registrarUsuario(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
        return render(request, 'registration/register.html', {'form': form})
