from django import forms
from .models import User
from django.contrib.auth import authenticate

class UserRegisterForm(forms.ModelForm):
    """Form definition for UserRegister."""

    password1 = forms.CharField(
        label="Password",
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder':'Password'
            }
        )
    )
    password2 = forms.CharField(
        label="Password (repeat)",
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder':'Repeat Password'
            }
        )
    )

    class Meta:
        """Meta definition for UserRegisterform."""
        model = User
        fields = ('username','email','names','lastname','gender')

    def clean_password2(self):
        if self.cleaned_data['password1'] != self.cleaned_data['password2']:
            self.add_error('password2','Las contraseñas no coinciden')

class LoginForm(forms.Form):
    username = forms.CharField(
        label="Username",
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder':'Nombre de usuario',
                'style': '{ margin: 10px }',
            }
        )
    )
    password = forms.CharField(
        label="Password (repeat)",
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder':'Password'
            }
        )
    )

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']

        if not authenticate(username= username, password=password):
            raise forms.ValidationError('Los datos no son correctos')

        return self.cleaned_data

class UpdatePasswordForm(forms.Form):
    password1 = forms.CharField(
        label="Password (actual)",
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder':'Contraseña Actual'
            }
        )
    )
    password2 = forms.CharField(
        label="Password (nueva)",
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder':'Contraseña Nueva'
            }
        )
    )

class VerificationForm(forms.Form):
    cod_reg = forms.CharField(required=True)

    def __init__(self, pk, *args, **kwargs):
        self.id_user = pk
        super(VerificationForm, self).__init__(*args, **kwargs)

    def clean_cod_reg(self):
        code = self.cleaned_data['cod_reg']

        if len(code) == 6:
            active = User.objects.cod_validation(
                self.id_user,
                code
            )
            if not active:
                raise forms.ValidationError('Codigo no valido')
        else:
            raise forms.ValidationError('Codigo no valido')