from django.contrib.auth.models import User
from django import forms

from utils import utils_accounts

class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'username', 'password', 'confirm_password'
        ]

    username = forms.CharField(
        max_length=25,
        label='Nome de usuário:',
        required=False,
    )
    username.widget.attrs.update({'class': 'teste'})

    password = forms.CharField(
        max_length=25,
        required=False,
        widget=forms.PasswordInput(),
        label='Senha:',
    )

    confirm_password = forms.CharField(
        max_length=25,
        required=False,
        widget=forms.PasswordInput(),
        label='Confirmar senha:',
    )

    def __init__(self, method,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.method = method

    def clean(self, *args, **kwargs):
        if not self.method == "POST":
            return super().clean(*args, **kwargs)

        error_msgs = utils_accounts.validation_fields(self.cleaned_data)

        if error_msgs:
            raise forms.ValidationError(error_msgs)

        return super().clean(*args, **kwargs)


class LoginForm(forms.Form):
    class Meta:
        model = User
        fields = [
            'username',
            'password',
        ]
        exclude = ['email']
    
    username = forms.CharField(
        max_length=25,
        label="Nome de usuário:",
        required=False,
    )

    password = forms.CharField(
        max_length=25,
        label='Senha:',
        widget=forms.PasswordInput(),
        required=False,
    )
    
    def __init__(self, method,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.method = method

    def clean(self, *args, **kwargs):
        error_msgs = {}
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if not username:
            error_msgs.update({'username': 'Nome de usuário inválido.'})

        if not password:
            error_msgs.update({'password': 'Senha inválida.'})

        if error_msgs and self.method == "POST":
            raise forms.ValidationError(error_msgs)

        return super().clean(*args, **kwargs)
