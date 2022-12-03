from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate 
from django.core.paginator import Paginator
from .models import Post
from .forms import PostForm



# Create your views here.
def index(request):
    posts = Post.objects.all()
    paginator = Paginator(posts, 2)
    num_pagina = request.GET.get('page')
    pagina_actual = paginator.get_page(num_pagina)
    return render(request,'index.html', {'posts': pagina_actual})

def crearPost(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
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

def verPost(request, pk):
    post = Post.objects.get(id=pk)
    tieneLike = request.user in post.likes.all()
    return render(request, 'post.html', {'post': post, 'likes': post.cantidadLIkes(), 'tieneLike': tieneLike})

def actualizarPost(request, pk):
    post = Post.objects.get(id=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post.save()
            return redirect('index')
    else:
        form = PostForm(instance=post)
        return render(request, 'creacion.html', {'form': form})

def eliminarPost(request, pk):
    post = Post.objects.get(id=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('index')
    return render(request, 'eliminar.html', {'post': post}) 

def darLike(request, pk):
    post = get_object_or_404(Post, id=pk)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return redirect('/post/' + str(post.id))
