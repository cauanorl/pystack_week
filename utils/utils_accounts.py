from django.contrib.auth.models import User
from django.contrib import auth


def check_username(new_username, old_username=None):
    username_errors = {}
    
    username_already_exists = User.objects.filter(
        username=new_username,
    )

    if old_username != new_username:
        if username_already_exists:
            username_errors.update(
                {'username': 'Esse nome de usuário ja está em uso.'})

    if not new_username:
        username_errors.update(
            {'username': 'Nome de usuário não pode ser em branco.'})
    elif new_username[0].isnumeric():
        username_errors.update(
            {'username': 'O nome não pode ser iniciado com números.'})

    if len(new_username) < 6:
        username_errors.update(
            {'username': 'Nome de usuário não pode ser menor que 6 caracteres.'})
    
    return username_errors


def validate_password(password, confirm_password):
    password_errors = {}

    if password != confirm_password:
        password_errors.update({'confirm_password': 'As senhas não conferem.'})
    
    if len(password) < 6:
        password_errors.update(
            {'password': 'Senha não pode ser menor que 6 caracters.'})
    
    if not password:
        password_errors.update({'password': 'Senha não pode ser em branco.'})

    return password_errors


def validation_fields(cleaned_data):
    error_msgs = {}
    
    username = cleaned_data.get('username').strip()
    password = cleaned_data.get('password').strip()
    confirm_password = cleaned_data.get('confirm_password').strip()

    error_msgs.update(check_username(username))
    error_msgs.update(validate_password(password, confirm_password))

    return error_msgs


def create_and_login_account(request, username, password):
    user = User.objects.create_user(
        username=username, password=password,
    )
    user.save()
    user = auth.authenticate(
        request, username=username, password=password)

    auth.login(request, user)
