from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, UserLoginForm, PaymentForm
from .models import Account, User, Transaction
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import transaction
from datetime import datetime
from .exchange_rate import get_exchange_rate
from django.core.cache import cache
import pytz


def home(request):
    auth_user = request.user.is_authenticated
    try:
        username = request.user.first_name
    except AttributeError:
        username = 'Guest'

    uah_to_usd_rate, uah_to_eur_rate = get_exchange_rate()

    uah_to_usd_rate = str(uah_to_usd_rate)[:-2]
    uah_to_eur_rate = str(uah_to_eur_rate)[:-2]

    common_context = get_common_context(request)
    return render(request, 'banking/home.html',
                  {'auth_user': auth_user,
                   'username': username,
                   'uah_to_usd_rate': uah_to_usd_rate,
                   'uah_to_eur_rate': uah_to_eur_rate,
                   **common_context})


def get_common_context(request):
    user_timezone = get_user_timezone(request)
    current_time = datetime.now(pytz.timezone(user_timezone))
    time_of_day = get_time_of_day(current_time)

    return {
        'time_of_day': time_of_day,
    }


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
    balance = Account.objects.get(user=request.user).balance
    last_name = request.user.last_name
    email = Account.objects.get(user=request.user).user.email

    common_context = get_common_context(request)
    uah_to_usd_rate, uah_to_eur_rate = get_exchange_rate()
    uah_balance = round(float(balance) * float(uah_to_usd_rate), 2)

    return render(request, 'banking/cabinet.html', {'username': username, 'last_name': last_name,
                                                    'balance': balance,
                                                    'email': email, 'uah_balance': uah_balance, **common_context})


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
    elif 18 <= hour < 23:
        return 'Good evening'
    else:
        return 'Good night'


@transaction.atomic
def transfer(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            recipient = form.cleaned_data['email']
            amount = form.cleaned_data['amount']

            if User.objects.filter(username=recipient).exists():
                try:
                    with transaction.atomic():
                        # Проверяем есть ли деньги на счету у переводящего
                        if amount > request.user.account.balance:
                            messages.error(request, 'Insufficient funds.')
                            return redirect('transfer')

                        # Уменьшаем баланс отправителя
                        request.user.account.balance -= amount
                        request.user.account.save()

                        # Увеличиваем баланс получателя
                        recipient_account = Account.objects.get(user__username=recipient)
                        recipient_account.balance += amount
                        recipient_account.save()

                        # Создаем запись о транзакции
                        Transaction.create_transaction(sender=request.user.account,
                                                       receiver=recipient_account, amount=amount)

                        return redirect('success_transfer')

                except Exception as e:
                    messages.error(request, f'Transaction failed: {str(e)}')
            else:
                messages.error(request, 'Account not found.')

    return render(request, 'banking/transfer.html')


def success_transfer(request):
    return render(request, 'banking/success_transfer.html')