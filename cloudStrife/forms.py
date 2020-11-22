from django import forms

class FormularioLogin(forms.Form):
    usuario=forms.CharField(required=True)
    contra=forms.CharField(widget=forms.PasswordInput(), required=True)

class FormularioRegistro(forms.Form):
    usuario=forms.CharField(required=True)
    contra=forms.CharField(widget=forms.PasswordInput(), required=True)
    contra1=forms.CharField(widget=forms.PasswordInput(), required=True)
    email=forms.EmailField(required=True)