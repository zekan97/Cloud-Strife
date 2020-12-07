from django import forms

class FormularioLogin(forms.Form):
    usuario=forms.CharField(required=True)
    contra=forms.CharField(widget=forms.PasswordInput(), required=True, label="Contraseña")

class FormularioRegistro(forms.Form):
    usuario=forms.CharField(required=True)
    contra=forms.CharField(widget=forms.PasswordInput(), required=True, label="Contraseña")
    contra1=forms.CharField(widget=forms.PasswordInput(), required=True, label="Confirmar contraseña")
    email=forms.EmailField(required=True)