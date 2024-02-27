from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('login/', views.login, name='login'),
    path('signup/', views.register, name='register'),
    path('success_account/', views.success_account, name='success_account'),
]