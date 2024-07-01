from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import CustomUserCreationForm
from .models import CustomUser
from django.contrib.auth.decorators import login_required

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            if 'profile_picture' in request.FILES:
                user.profile_picture = request.FILES['profile_picture']
            if 'is_patient' in request.POST:
                user.is_patient = True
            elif 'is_doctor' in request.POST:
                user.is_doctor = True
            user.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'apps/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'apps/login.html', {'error': 'Invalid username or password'})
    return render(request, 'apps/login.html')






def dashboard(request):
    user = request.user
    if user.is_patient:
        return render(request, 'apps/patient_dashboard.html', {'user': user})
    elif user.is_doctor:
        return render(request, 'apps/doctor_dashboard.html', {'user': user})