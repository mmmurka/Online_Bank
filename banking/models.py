from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=20)
    balance = models.IntegerField(default=0)
    identification_number = models.PositiveIntegerField(
        default=10,
        unique=True,
        validators=[MinValueValidator(1000000)],
        db_comment='Personal identification number with 8 digits'
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}'s Account"