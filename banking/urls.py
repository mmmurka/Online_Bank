from django.urls import path
from django.contrib.auth import views as auth_views
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
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]


