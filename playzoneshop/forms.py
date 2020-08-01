from django import forms
from django.contrib.auth.models import User

class RegisterForm(forms.Form):
    username = forms.CharField(required=True, 
                                widget=forms.TextInput(attrs={
                                    'class': 'form-control',
                                    'placeholder': 'Nombre Usuario',
                                    'id': 'username',

                                }))
    email = forms.EmailField(required=True, 
                                widget=forms.EmailInput(attrs={
                                    'class': 'form-control',
                                    'placeholder': 'Email',
                                    'id': 'email',

                                }))
    password = forms.CharField(required=True, 
                                widget=forms.PasswordInput(attrs={
                                    'class': 'form-control',
                                    'placeholder': 'Contraseña', 
                                    'id': 'password',

                                }))
    password2 = forms.CharField(required=True, 
                                widget=forms.PasswordInput(attrs={
                                    'class': 'form-control',
                                    'placeholder': 'Confirmar contraseña', 

                                }))

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('El nombre de usuario ya está en uso')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Dirección de email ya está en uso')
        return email

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('password2') != cleaned_data.get('password'):
            self.add_error('password2', 'Confirmación de contraseña no coincide')

    def save(self):
        return User.objects.create_user(
            self.cleaned_data.get('username'),
            self.cleaned_data.get('email'),
            self.cleaned_data.get('password'),
        )