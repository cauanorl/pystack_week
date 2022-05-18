from django.urls import path
from . import views


app_name = "jobs"

urlpatterns = [
    path('', views.Jobs.as_view(), name='list_jobs'),
    path('accept_job/<int:id>', views.accept_job, name='accept_job'),
    path('profile/', views.Profile.as_view(), name='profile'),
    path('send_project/', views.send_project, name='send_project'),
]
