from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from cloudStrife.forms import FormularioLogin, FormularioRegistro
from cloudStrife.models import Usuario, Foto, Comentario, Seguidore
from passlib.hash import pbkdf2_sha256
from django.core.files.storage import FileSystemStorage
from datetime import datetime
import os

# Create your views here.

def login(request):
    if request.method=="POST":
        login=FormularioLogin(request.POST)
        if login.is_valid():
            user=request.POST["usuario"]
            contra=request.POST["contra"]
            credenciales=Usuario.objects.filter(usuario__iexact=user)
            if credenciales:
                passAComprobar=Usuario.objects.values_list('password', flat=True).get(usuario=user)
                if pbkdf2_sha256.verify(contra, passAComprobar ):
                    request.session['login'] = user
                    render(request, "inicio.html", {"usuario": user})
                    return redirect('usuario', user)
                else:
                    messages.error(request, 'Contraseña incorrecta')
                    return render(request, "login.html", {"form":login})
            else:
                messages.error(request, 'Este usuario no existe')
                return render(request, "login.html", {"form":login})           
    else:
        login=FormularioLogin()

    return render(request, "login.html", {"form":login})

def registro(request):
    if request.method=="POST":
        registro=FormularioRegistro(request.POST)

        if registro.is_valid():

            #Recogemos los datos del formulario
            user=request.POST["usuario"]
            contra=request.POST["contra"]
            contra1=request.POST["contra1"]
            email=request.POST["email"]

            #Comprobamos si hay algun usuario o e-mail repetido
            usuario=Usuario.objects.filter(usuario=user)
            email_usuario=Usuario.objects.filter(email=email)

            #Hacemos las comprobaciones para insertar el usuario
            # Usuario unico, contraseñas iguales e e-mail único tambien
            if usuario:
                messages.error(request, 'Este usuario ya existe')
                return render(request, "registro.html", {"form":registro})
            else:
                if contra != contra1:
                    messages.error(request, 'Las contraseñas no son iguales')
                    return render(request, "registro.html", {"form":registro})
                else:
                    if email_usuario:
                        messages.error(request, 'Este e-mail ya ha sido dado de alta')
                        return render(request, "registro.html", {"form":registro})
                    else:                        
                        contra_cifrada=pbkdf2_sha256.encrypt(contra, rounds=12000, salt_size=32)
                        usuarioInsertar=Usuario(usuario=user, password=contra_cifrada, email=email)
                        usuarioInsertar.save()
                        return redirect('/login/')
    else:
        registro=FormularioRegistro()
    return render(request, "registro.html", {"form":registro})

def inicio(request, usuario):
    p = Usuario.objects.filter(usuario_seguido__seguidor=usuario)
    fotos = Foto.objects.filter(creador__in=p).order_by('-fecha')
    return render(request, "inicio.html", {"usuario": usuario, "fotos": fotos})


def explorar(request, usuario):
    p = Usuario.objects.filter(usuario_seguido__seguidor=usuario)
    fotos_explorar = Foto.objects.exclude(creador__in=p).exclude(creador=usuario)
    return render(request, "explorar.html", {"usuario": usuario, "fotos_explorar":fotos_explorar})

def perfil(request, usuario):
    datos_perfil=Usuario.objects.get(usuario=usuario)
    fotos=Foto.objects.filter(creador=usuario)
    seguidores=Seguidore.objects.filter(usuario_seguido=usuario).count()
    seguidos=Seguidore.objects.filter(seguidor=usuario).count()
    return render(request, "perfil.html", {"usuario": usuario, "datos_perfil": datos_perfil, "fotos": fotos, "seguidos": seguidos, "seguidores": seguidores})

def preferencias(request, usuario):
    if request.method=='POST':
        uploaded_file = request.FILES.get('avatar', False)
        biografia = request.POST.get('biografia', False)
        user=Usuario.objects.get(usuario=usuario)
        if biografia:
            user.biografia = biografia
        if uploaded_file:
            file_name, file_extension = os.path.splitext(uploaded_file.name)           
            if file_extension == ".png" or file_extension == ".jpg":
                nuevo_nombre = usuario + "-avatar" + file_extension
                fs = FileSystemStorage()
                if fs.exists(nuevo_nombre):
                    fs.delete(nuevo_nombre)
                fs.save(nuevo_nombre, uploaded_file)                
                user.avatar=nuevo_nombre
        user.save()
        return redirect('perfil', usuario)      
    return render(request, "preferencias.html", {"usuario": usuario})

def foto(request, usuario):
    if request.method=='POST':
        uploaded_file = request.FILES['foto']
        titulo_foto = request.POST['titulo']
        file_name, file_extension = os.path.splitext(uploaded_file.name)
        fecha = datetime.now()
        if file_extension == ".png" or file_extension == ".jpg":
            if Foto.objects.filter(creador=usuario).count() == 0:
                nombre_foto = usuario + '_1' + file_extension
            else:
                fotos = Foto.objects.filter(creador=usuario).count() + 1
                fotos_string = str(fotos) 
                nombre_foto = usuario + "_" + fotos_string + file_extension
            fs = FileSystemStorage()
            fs.save(nombre_foto, uploaded_file)
            usuario_creador=Usuario.objects.get(usuario=usuario)
            foto = Foto(titulo=titulo_foto, foto=nombre_foto, fecha=fecha, creador=usuario_creador)
            foto.save() 
            return redirect('usuario', usuario)               
    return render(request, "foto.html", {"usuario": usuario})

def foto_comentarios(request, usuario, id_foto):
    datos_perfil=Usuario.objects.get(usuario=usuario)
    foto=Foto.objects.get(id=id_foto)
    comentarios=Comentario.objects.filter(foto_comentada=id_foto)
    

    if request.method=='POST':
        texto_comentario=request.POST['comentario'] 
        fecha = datetime.now()
        insertar_comentario=Comentario(comentario=texto_comentario, fecha=fecha, foto_comentada=foto, usuario_creador=usuario)
        insertar_comentario.save()
    return render(request, "comentarios.html", {"usuario": usuario, "id_foto": id_foto, "comentarios": comentarios, "foto":foto, "datos_perfil": datos_perfil,})

def buscar(request, usuario):
    usuarios_no_seguidos=Usuario.objects.exclude(usuario=usuario).exclude(usuario_seguido__seguidor=usuario)
    if request.method=='POST':
        criterio_busqueda=request.POST['buscar']
        usuarios_buscados=Usuario.objects.exclude(usuario=usuario).filter(usuario__icontains=criterio_busqueda)       
        return render(request, "buscar.html", {"usuario": usuario, "usuarios_buscados":usuarios_buscados, "criterio_busqueda": criterio_busqueda})
    return render(request, "buscar.html", {"usuario": usuario, "usuarios_no_seguidos": usuarios_no_seguidos})

def perfil_buscado(request, usuario, usuario_buscado):
    datos_perfil_buscado=Usuario.objects.get(usuario=usuario_buscado)
    fotos_perfil_buscado=Foto.objects.filter(creador=usuario_buscado)
    relacion_seguidor=Seguidore.objects.filter(seguidor=usuario, usuario_seguido=datos_perfil_buscado).first()
    seguidores=Seguidore.objects.filter(usuario_seguido=usuario_buscado).count()
    seguidos=Seguidore.objects.filter(seguidor=usuario_buscado).count()

    if request.method=="POST":
        if request.POST['seguido'] == "0":
            seguidor=Usuario.objects.get(usuario=usuario)
            seguido=Usuario.objects.get(usuario=usuario_buscado)
            nuevo_follow=Seguidore(seguidor=seguidor, usuario_seguido=seguido)
            nuevo_follow.save()
        else:
            unfollows=Seguidore.objects.filter(seguidor=usuario, usuario_seguido=datos_perfil_buscado).first()
            unfollows.delete()
    return render(request, "perfil_buscado.html", {"usuario":usuario, "seguidores": seguidores, "seguidos":seguidos, "usuario_buscado": usuario_buscado, "datos_perfil_buscado": datos_perfil_buscado, "fotos_perfil_buscado": fotos_perfil_buscado, "relacion_seguidor": relacion_seguidor})

def foto_perfil_buscado(request, usuario, usuario_buscado, id_foto):
    datos_perfil_buscado=Usuario.objects.get(usuario=usuario_buscado)
    foto_perfil_buscado=Foto.objects.get(id=id_foto)
    comentarios=Comentario.objects.filter(foto_comentada=id_foto)
    return render(request, "foto_perfil_buscado.html", {"usuario":usuario, "usuario_buscado": usuario_buscado, "id_foto": id_foto, "datos_perfil_buscado": datos_perfil_buscado, "foto_perfil_buscado": foto_perfil_buscado, "comentarios":comentarios})

def seguidores(request, usuario):
    seguidores=Seguidore.objects.filter(usuario_seguido=usuario)
    return render(request, "seguidores.html", {"usuario":usuario, "seguidores": seguidores})

def seguidos(request, usuario):
    seguidos=Seguidore.objects.filter(seguidor=usuario)
    return render(request, "seguidos.html", {"usuario":usuario, "seguidos": seguidos})

def seguidos_buscados(request, usuario, usuario_buscado):
    seguidos=Seguidore.objects.filter(seguidor=usuario_buscado)
    return render(request, "seguidos_buscados.html", {"usuario":usuario, "usuario_buscado": usuario_buscado, "seguidos": seguidos})

def seguidores_buscados(request, usuario, usuario_buscado):
    seguidores=Seguidore.objects.filter(usuario_seguido=usuario_buscado)
    return render(request, "seguidores_buscados.html", {"usuario":usuario, "usuario_buscado": usuario_buscado, "seguidores": seguidores})