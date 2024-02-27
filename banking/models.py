from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.IntegerField(default=0)
