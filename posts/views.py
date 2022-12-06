from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate 
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.core.paginator import Paginator
from .models import Post
from .forms import PostForm

from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
import threading

# Create your views here.
def index(request):
    posts = Post.objects.all()
    paginator = Paginator(posts, 3)
    num_pagina = request.GET.get('page')
    pagina_actual = paginator.get_page(num_pagina)
    return render(request,'index.html', {'posts': pagina_actual})

@login_required(login_url='login')
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

@login_required(login_url='login')
def verPost(request, pk):
    post = get_object_or_404(Post, id=pk)
    tieneLike = request.user in post.likes.all()
    return render(request, 'post.html', {'post': post, 'likes': post.cantidadLIkes(), 'tieneLike': tieneLike})

@login_required(login_url='login')
def actualizarPost(request, pk):
    post = get_object_or_404(Post, id=pk)
    if post.autor == request.user:
        if request.method == 'POST':
            form = PostForm(request.POST, request.FILES, instance=post)
            if form.is_valid():
                post.save()
                return redirect('index')
        else:
            form = PostForm(instance=post)
            return render(request, 'creacion.html', {'form': form})
    else: 
        return redirect(f'/post/{post.id}')


@login_required(login_url='login')
def eliminarPost(request, pk):
    post = get_object_or_404(Post, id=pk)
    if post.autor == request.user:
        if request.method == 'POST':
            post.delete()
            return redirect('index')
        return render(request, 'eliminar.html', {'post': post})
    else: 
        return redirect(f'/post/{post.id}')


@login_required(login_url='login')
def darLike(request, pk):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=pk)
        if request.user in post.likes.all():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)
        return redirect('/post/' + str(post.id))
    else:
        raise Http404()


# Envio de correo 
# Tuturial: https://www.youtube.com/watch?v=e7NEpX12xDI&t=1801s&ab_channel=codigofacilito
def index2(request):
    return render(request, 'index2.html', {})

def create_mail(email, subject, template_path,  context):
    template = get_template(template_path)
    content = template.render(context)

    mail = EmailMultiAlternatives(
        subject= subject,
        body='',
        from_email='enaranjoc.en99@gmail.com',
        to=[email]
    )
    mail.attach_alternative(content, 'text/html')
    return mail


def send_welcome_mail():
    welcome_mail = create_mail(
        'ariel99.en@gmail.com',
        'Prueba de django',
        'welcome.html',
        {
            'username':'Erick Naranjo'
        }
    )

    welcome_mail.send(fail_silently=False)

def send_mail(request):
    thread = threading.Thread(
        target=send_welcome_mail
    )
    thread.start()
    return redirect('index2')