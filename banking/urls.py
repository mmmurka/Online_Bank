from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.user_login, name='login'),
    path('signup/', views.register, name='register'),
    path('success_account/', views.success_account, name='success_account'),
    path('cabinet/', views.cabinet, name='cabinet'),
    path('logout/', views.user_logout, name='logout'),
    path('transfer/', views.transfer, name='transfer'),
    path('success_transfer/', views.success_transfer, name='success_transfer'),
]