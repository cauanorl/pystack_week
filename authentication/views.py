from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib import messages

from django.urls import reverse
from django.shortcuts import render, redirect
from django.views.generic import View

from utils import utils_accounts

from . import forms

# Create your views here.
class Login(View):
    template_name = 'authentication/login.html'

    def setup(self, *args, **kwargs) -> None:
        super().setup(*args, **kwargs)
        self.context = {
            'loginform': forms.LoginForm(
                self.request.method,
                data=self.request.POST,
            )
        }


    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('jobs:list_jobs')
        return render(request, self.template_name, self.context)
    
    def post(self, *args, **kwargs):
        data = self.request.POST
        login_form = self.context.get('loginform')

        username = data.get('username')
        password = data.get('password')

        if login_form.is_valid():
            user = auth.authenticate(
                self.request, username=username, password=password)

            if user:
                auth.login(self.request, user)
            else:
                messages.error(
                    self.request, "Nome de usuário ou senha estão incorretos.")

        return redirect('login')


class Register(View):
    template_name = 'authentication/register.html'

    def setup(self, *args, **kwargs) -> None:
        super().setup(*args, **kwargs)

        self.context = {
            'registerform': forms.RegisterForm(
                self.request.method,
                data=self.request.POST,
            )
        }

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect(reverse('login'))

        return render(request, self.template_name, self.context)

    def post(self, *args, **kwargs):
        form = self.context.get('registerform')
        username = self.request.POST.get('username').strip()
        password = self.request.POST.get('password').strip()

        if self.request.user.is_authenticated:
            return redirect(reverse('login'))

        if form.is_valid():
            try:                
                utils_accounts.create_and_login_account(
                    self.request,
                    username,
                    password,
                )

                return redirect('login')
            except:
                messages.error(self.request, 'Ocorreu um erro no sistema.')

        return render(self.request, self.template_name, self.context)


def logout(request):
    auth.logout(request)
    return redirect('login')
