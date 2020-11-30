from django.db import models

# Create your models here.

class Usuario(models.Model):
    usuario=models.CharField(max_length=30, primary_key=True)
    password=models.CharField(max_length=1000)
    email=models.EmailField()
    avatar=models.CharField(max_length=200, null=False, default="defaul-avatar.png")
    biografia=models.CharField(max_length=200, null=True)

class Foto(models.Model):
    titulo=models.CharField(max_length=200, null=True)
    foto=models.CharField(max_length=200, null=False)
    fecha=models.DateField(null=False)
    creador=models.ForeignKey(Usuario, on_delete=models.CASCADE)

class Comentario(models.Model):
    comentario=models.CharField(max_length=1000, null=False)
    fecha=models.DateField(null=False)
    foto_comentada=models.ForeignKey(Foto, on_delete=models.CASCADE)
    usuario_creador=models.CharField(max_length=30)

class Seguidore(models.Model):
    usuario_seguido=models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="usuario_seguido")
    seguidor=models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="seguidor")
    
