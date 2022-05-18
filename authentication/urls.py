from django.urls import path, reverse_lazy
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('',  views.Login.as_view()),
    path('login/', views.Login.as_view(), name='login'),
    path('register/', views.Register.as_view(), name='register'),
    path('logout/', views.logout, name='logout'),

    # Redefinir senha
    path(
        'password_reset/',
        auth_views.PasswordResetView.as_view(
            template_name='authentication/password_reset.html'),
        name='password_reset',
    ),

    path(
        'password_reset_done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='authentication/password_reset_done.html'),
        name='password_reset_done',
    ),

    path(
        'password_reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='authentication/password_reset_confirm_view.html'),
        name='password_reset_confirm',
    ),

    path(
        'password_reset_complete/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='authentication/password_reset_complete.html'),
        name='password_reset_complete',

    )
]
