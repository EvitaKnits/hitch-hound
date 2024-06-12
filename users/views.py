from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import CustomUserCreationForm

# Create your views here.

def user_login(request):
    return render(request, 'login.html')

def user_logout(request):
    return render(request, 'logout.html', {'active_page': 'logout'})

def user_signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})

def password_reset(request):
    return render(request, 'reset.html')

def user_profile(request):
    return render(request, 'profile.html', {'active_page': 'profile'})