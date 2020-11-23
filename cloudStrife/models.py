from django.db import models

# Create your models here.
class Usuario(models.Model):
    usuario=models.CharField(max_length=30, primary_key=True)
    password=models.CharField(max_length=1000)
    email=models.EmailField()
    avatar=models.CharField(max_length=200, null=False, default="../../media/defaul-avatar.png")
    biografia=models.CharField(max_length=200, null=True)

class Foto(models.Model):
    titulo=models.CharField(max_length=200, null=True)
    foto=models.CharField(max_length=200, null=False)
    fecha=models.DateField()
    creador=models.ForeignKey(Usuario, on_delete=models.CASCADE)
    
