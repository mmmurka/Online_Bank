from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, UserLoginForm
from .models import Account, User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime
import pytz


def home(request):
    auth_user = request.user.is_authenticated
    username = request.user.first_name
    user_timezone = get_user_timezone(request)
    current_time = datetime.now(pytz.timezone(user_timezone))
    time_of_day = get_time_of_day(current_time)
    context = {'time_of_day': time_of_day}
    return render(request, 'banking/home.html', {'auth_user': auth_user, 'username': username, **context})


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
            messages.error(request, form.errors)
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


@login_required
def cabinet(request):
    username = request.user.first_name
    return render(request, 'banking/cabinet.html', {'username': username})


def user_logout(request):
    logout(request)
    return redirect('home')


def get_user_timezone(request):
    # Получение информации о часовом поясе пользователя из request
    # Здесь можно использовать, например, информацию из cookies или профиля пользователя
    # В данном примере используется часовой пояс сервера в случае отсутствия информации от пользователя
    return request.COOKIES.get('user_timezone', 'UTC')


def get_time_of_day(current_time):
    hour = current_time.hour
    if 6 <= hour < 12:
        return 'Good morning'
    elif 12 <= hour < 18:
        return 'Have a nice day'
    elif 18 <= hour < 24:
        return 'Good evening'
    else:
        return 'Good night'