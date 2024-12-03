from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Job, Company
from .forms import JobForm


# Create your views here.

# LOGIN VIEW
def loginPage(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username OR Password does not exist')

    context = {}
    return render(request, 'base/login_register.html', context)

# LOGOUT VIEW
def logoutUser(request):
    logout(request)
    return redirect('home')


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    
    jobs = Job.objects.filter(
        Q(company__name__icontains=q) |
        Q(title__icontains=q) |
        Q(description__icontains=q)
        )
    companies = Company.objects.all()
    job_count = jobs.count()

    context = {'jobs': jobs, 'companies': companies, 'job_count': job_count}
    return render(request, 'base/home.html', context)

def job(request, pk):
    job = Job.objects.get(id=pk)
    context = {'job': job}        
    return render(request, 'base/job.html', context)

def createJob(request):
    form = JobForm()
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'base/job_form.html', context)

def updateJob(request, pk):
    job = Job.objects.get(id=pk)
    form = JobForm(instance=job)

    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/job_form.html', context)

def deleteJob(request, pk):
    job = Job.objects.get(id=pk)
    if request.method == 'POST':
        job.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': job})