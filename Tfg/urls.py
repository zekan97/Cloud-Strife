"""Tfg URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path
from cloudStrife import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.login, name="index"),
    path('login/', views.login, name="login"),
    path('registro/', views.registro, name="registro"),
    path('inicio/<str:usuario>', views.inicio, name="usuario"),
    path('explorar/<str:usuario>', views.explorar, name="explorar"),
    path('perfil/<str:usuario>', views.perfil, name="perfil"),
    path('preferencias/<str:usuario>', views.preferencias, name="preferencias"),
    path('foto/<str:usuario>', views.foto, name="foto"),
    path('buscar/<str:usuario>', views.buscar, name="buscar"),
    path('foto_comentarios/<str:usuario>/<int:id_foto>', views.foto_comentarios, name="comentarios"),
    path('perfil_buscado/<str:usuario>/<str:usuario_buscado>', views.perfil_buscado, name="perfil_buscado"),
    path('foto_perfil_buscado/<str:usuario>/<str:usuario_buscado>/<int:id_foto>', views.foto_perfil_buscado, name="foto_perfil_buscado"),
    path('seguidores/<str:usuario>', views.seguidores, name="seguidores"),
    path('seguidos/<str:usuario>', views.seguidos, name="seguidos"),
    path('seguidos_buscado/<str:usuario>/<str:usuario_buscado>', views.seguidos_buscados, name="seguidos_buscados"),
    path('seguidores_buscado/<str:usuario>/<str:usuario_buscado>', views.seguidores_buscados, name="seguidores_buscados"),
    path('admin/', admin.site.urls),
]

urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
