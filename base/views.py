from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .models import Job, Company
from .forms import JobForm


# Create your views here.

# LOGIN VIEW
def loginPage(request):

    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
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

    context = {'page': page}
    return render(request, 'base/login_register.html', context)

# LOGOUT VIEW
def logoutUser(request):
    logout(request)
    return redirect('home')

# REGISTER PAGE VIEW
def registerPage(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'A error occurred during registration.')

    return render(request, 'base/login_register.html', {'form': form})

# HOME VIEW
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

# JOB VIEW
def job(request, pk):
    job = Job.objects.get(id=pk)
    context = {'job': job}        
    return render(request, 'base/job.html', context)

@login_required(login_url='login')
def createJob(request):
    form = JobForm()
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'base/job_form.html', context)

# PROFILE VIEW
def userProfile(request, pk):
    user = User.objects.get(id = pk)
    context = {'user': user}
    return render(request, 'base/profile.html', context)

@login_required(login_url='login')
def updateJob(request, pk):
    job = Job.objects.get(id=pk)
    form = JobForm(instance=job)

    # restrict others from updating others Jobs
    if request.user != Job.host:
        return HttpResponse('You are not allowed here')

    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/job_form.html', context)

@login_required(login_url='login')
def deleteJob(request, pk):
    job = Job.objects.get(id=pk)

    # restrict others from deleting others Jobs
    if request.user != Job.host:
        return HttpResponse('You are not allowed here')
    
    if request.method == 'POST':
        job.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': job})