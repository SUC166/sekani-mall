from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomerRegistrationForm, CustomerUpdateForm
from .models import CustomUser

def register(request):
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Welcome to SEKANI Mall!')
            return redirect('product_list')
    else:
        form = CustomerRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

def customer_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user and user.role == 'customer':
            login(request, user)
            return redirect('product_list')
        else:
            messages.error(request, 'Invalid credentials.')
    return render(request, 'accounts/login.html')

def sekani_admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user and user.is_sekani_admin():
            login(request, user)
            return redirect('dashboard_home')
        else:
            messages.error(request, 'Invalid SEKANI admin credentials.')
    return render(request, 'accounts/admin_login.html')

def logout_view(request):
    logout(request)
    return redirect('product_list')

@login_required
def profile(request):
    if request.method == 'POST':
        form = CustomerUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated!')
            return redirect('profile')
    else:
        form = CustomerUpdateForm(instance=request.user)
    return render(request, 'accounts/profile.html', {'form': form})
