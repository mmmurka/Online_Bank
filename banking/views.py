from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from .models import Account, User
from django.contrib import messages


def home(request):
    return render(request, 'banking/home.html')


def login(request):
    return render(request, 'banking/login.html')


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
                                            password=form.cleaned_data['password'])

            # Создаем запись в таблице Account
            account = Account.objects.create(user=user)

            # Перенаправляем на страницу успеха
            return redirect('success_account')
        else:
            messages.error(request, 'Invalid data.')
    return render(request, 'banking/signup.html')


def success_account(request):
    return render(request, 'banking/signup_done.html')



