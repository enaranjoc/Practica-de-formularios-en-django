"""mipagina URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from posts import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('crear/', views.crearPost, name='crear'),
    path('', include('django.contrib.auth.urls')), # url propia de django para obtener las rutas de login y logout
    path('registrarse/', views.registrarUsuario, name='registrarUsuario'),
    path('post/<int:pk>', views.verPost, name='verPost'),
    path('actualizar/<int:pk>', views.actualizarPost, name='actualizarPost'),
    path('eliminar/<int:pk>', views.eliminarPost, name='eliminarPost'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # Para trabajar con archivos
