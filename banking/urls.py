from django.urls import path
from .views import UserForgotPasswordView, UserPasswordResetConfirmView
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
    # Стандартные представления Django для сброса пароля
    path('password-reset/', UserForgotPasswordView.as_view(), name='password_reset'),
    path('set-new-password/<uidb64>/<token>/', UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]


