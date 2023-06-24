from django.shortcuts import render, redirect
from . models import  Profile

from django.contrib.auth.decorators import login_required


from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from . forms import ProfileForm, UpdateProfileForm
# Create your views here.
def register(request):
    form = ProfileForm()
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            cpassword = form.cleaned_data.get('password2')

            if password != cpassword:
                messages.warning(request, 'Password do not match')
                return redirect('register')
            if User.objects.filter(username=username).exists():
                messages.warning(request, 'Username already exists')
            if User.objects.filter(email=email).exists():
                messages.warning(request, 'Email already exists')
            
            user = User.objects.create_user(username,email,password)
            form = form.save(commit = False)
            form.user = user
            form.save()
            return redirect('login')

    context = {
        'form': form
    }
    return render(request, 'users/register.html', context)

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username = username, password = password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful')
            return redirect('myCart')
        else:
            messages.success(request, 'Incorrect username or password')
            return redirect('login')
            
    return render(request, 'users/login.html')

def logout_user(request):
    logout(request)
    messages.warning(request, 'Logout successful')
    return redirect('login')

@login_required(login_url = 'login')
def dashboard(request):
    users = request.user.profile

    context = {
        'users': users
    }

    return render(request, 'users/dashboard.html', context)

def update_profile(request):
    user = User.objects.get(username= request.user)
    users = request.user.profile
    update = UpdateProfileForm(instance= users)

    if request.method == 'POST':
        form = UpdateProfileForm(request.POST,request.FILES, instance= users)
        if form.is_valid():
            user.username = request.POST.get('username')
            user.email = request.POST.get('email')
            user.save()
            form.save()
            return redirect('dashboard')

    context = {
        'users': users,
        'form': update
    }
    return render(request, 'users/update_profile.html', context)