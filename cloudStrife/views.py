from django.shortcuts import render, redirect
from django.http import HttpResponse
from cloudStrife.forms import FormularioLogin, FormularioRegistro
from cloudStrife.models import Usuario, Foto
from passlib.hash import pbkdf2_sha256
from django.core.files.storage import FileSystemStorage
from datetime import datetime
import os

# Create your views here.

def login(request):
    if request.method=="POST":
        login=FormularioLogin(request.POST)
        #informacion=login.cleaned_data
        if login.is_valid():
            user=request.POST["usuario"]
            contra=request.POST["contra"]
            credenciales=Usuario.objects.filter(usuario__iexact=user)
            if credenciales:
                passAComprobar=Usuario.objects.values_list('password', flat=True).get(usuario=user)
                if pbkdf2_sha256.verify(contra, passAComprobar ):
                    render(request, "inicio.html", {"usuario": user})
                    return redirect('usuario', user)
                else:
                    print("Contraseña erronea")
                    return render(request, "login.html", {"form":login})
            else:
                print("Usuario erroneo")
                return render(request, "login.html", {"form":login})           
    else:
        login=FormularioLogin()

    return render(request, "login.html", {"form":login})

def registro(request):
    if request.method=="POST":
        registro=FormularioRegistro(request.POST)

        if registro.is_valid():
            #informacion=registro.cleaned_data
            
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
                print("nombre de usuario no valido")
                return render(request, "registro.html", {"form":registro})
            else:
                if contra != contra1:
                    print("contraseñas diferentes")
                    return render(request, "registro.html", {"form":registro})
                else:
                    if email_usuario:
                        print("Este e-mail ya esta registrado")
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
    return render(request, "inicio.html", {"usuario": usuario})

def explorar(request, usuario):
    return render(request, "explorar.html", {"usuario": usuario})

def perfil(request, usuario):

    datos_perfil=Usuario.objects.get(usuario=usuario)
    fotos = Foto.objects.filter(creador=usuario)

    return render(request, "perfil.html", {"usuario": usuario, "datos_perfil": datos_perfil, "fotos": fotos})

def preferencias(request, usuario):
    if request.method=='POST':
        uploaded_file = request.FILES['avatar']
        file_name, file_extension = os.path.splitext(uploaded_file.name)
        if file_extension == ".png" or file_extension == ".jpg":
            nuevo_nombre= usuario + "-avatar" + file_extension
            fs = FileSystemStorage()
            if fs.exists(nuevo_nombre):
                fs.delete(nuevo_nombre)
            fs.save(nuevo_nombre, uploaded_file)
            user=Usuario.objects.get(usuario=usuario)
            user.avatar="../../media/" + nuevo_nombre
            user.save()
            return redirect('perfil', usuario)
        else:
            print("archivo no subido")        
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
            nombre_bbdd = "../../media/" + nombre_foto
            usuario_creador=Usuario.objects.get(usuario=usuario)
            foto = Foto(titulo=titulo_foto, foto=nombre_bbdd, fecha=fecha, creador=usuario_creador)
            foto.save() 
            return redirect('usuario', usuario)               
    return render(request, "foto.html", {"usuario": usuario})
    