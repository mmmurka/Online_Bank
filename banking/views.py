from django.shortcuts import render

def home(request):
    return render(request, 'banking/home.html')


def login(request):
    return render(request, 'banking/login.html')


def signup(request):

    return render(request, 'banking/signup.html')


