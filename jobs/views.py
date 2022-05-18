
from typing import Any
from django.http import HttpRequest

from django.shortcuts import render, redirect, get_object_or_404

from django.views.generic import View
from django.views.generic.list import ListView

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from utils import utils_accounts
from . import models

# Create your views here.
class Jobs(ListView):
    template_name = 'jobs/list_jobs.html'
    model = models.Job
    context_object_name = 'jobs'

    def setup(self, request: HttpRequest, *args: Any, **kwargs: Any) -> None:
        super().setup(request, *args, **kwargs)
        self.user = request.user

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        query = super().get_queryset()
        query = query.filter(reserved=False)

        price_min = self.request.GET.get("price_min")
        if price_min:
            query = query.filter(price__gte=price_min) # Maior que,

        price_max = self.request.GET.get("price_max")
        if price_max:
            query = query.filter(price__lte=price_max) # Menor que,

        deadline_min = self.request.GET.get('deadline_min')
        if deadline_min:
            query = query.filter(delivery_time__gte=deadline_min) # Maior que,
        
        deadline_max = self.request.GET.get("deadline_max")
        if deadline_max:
            query = query.filter(delivery_time__lte=deadline_max) # Menor que,

        category = self.request.GET.get('category')
        if category:
            query = query.filter(category=category)

        return query


@login_required(redirect_field_name='login')
def accept_job(request, id):
    job = get_object_or_404(models.Job, id=id)
    job.professional = request.user
    job.reserved = True
    job.save()

    return redirect('jobs:list_jobs')


class Profile(View):
    template_name = 'jobs/profile.html'

    def setup(self, request: HttpRequest, *args: Any, **kwargs: Any) -> None:
        super().setup(request, *args, **kwargs)
        if not self.request.user.is_authenticated:
            self.render_template = redirect('login')
        else:
            jobs = models.Job.objects.filter(professional=self.request.user)

            self.context = {
                'jobs': jobs,
            }
            self.render_template = render(
                self.request, self.template_name, self.context)
    
    def get(self, request, *args, **kwargs):
        return self.render_template
    
    def post(self, request, *args, **kwargs):
        errors = {}

        datas = request.POST
        username = datas.get('username')
        email = datas.get('email')
        first_name = datas.get("first_name")
        last_name = datas.get('last_name')

        errors.update(
            utils_accounts.check_username(username, request.user.username))

        if errors:
            messages.error(request, 'Ocorreu um erro')
        else:
            user = get_object_or_404(User, username=request.user.username)
            user.username = username
            user.email = email
            user.first_name = first_name
            user.last_name = last_name

            user.save()

        return redirect('jobs:profile')


def send_project(request):
    file = request.FILES.get('file')
    job_id = request.POST.get('job_id')

    job = get_object_or_404(models.Job, id=job_id)

    if job:
        job.final_file = file
        job.status = "AA"
        job.save()

    return redirect('jobs:profile')
