from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, UserLoginForm
from .models import Account, User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout



def home(request):
    return render(request, 'banking/home.html')


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            if User.objects.filter(username__iexact=form.cleaned_data['email']).exists():
                messages.error(request, 'User with this email already exists.')
                return render(request, 'banking/signup.html', {'form': form})
            # Создаем пользователя
            user = User.objects.create_user(username=form.cleaned_data['email'].lower(),
                                            email=form.cleaned_data['email'],
                                            password=form.cleaned_data['password'],
                                            first_name=form.cleaned_data['first_name'],
                                            last_name=form.cleaned_data['last_name'])

            # Создаем запись в таблице Account
            account = Account.objects.create(user=user)

            # Перенаправляем на страницу успеха
            return redirect('success_account')
        else:
            messages.error(request, 'you invalid.')
    return render(request, 'banking/signup.html')


def user_login(request):
    if request.user.is_authenticated:
        return redirect('cabinet')
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['email'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('cabinet')
                else:
                    messages.error(request, 'account inactive')
            else:
                messages.error(request, 'invalid login')
    else:
        form = UserLoginForm()
    return render(request, 'banking/login.html', {'form': form})


def success_account(request):
    return render(request, 'banking/signup_done.html')


def cabinet(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'banking/cabinet.html')


def user_logout(request):
    logout(request)
    return redirect('home')

