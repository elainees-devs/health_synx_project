from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomUserCreationForm

def home(request):
    return render(request, "users/login.html")

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # automatically hashes password
            login(request, user)  # log in user after registration
            return redirect('home') 
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})
