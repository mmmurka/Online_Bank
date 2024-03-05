from django.db import models, transaction
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(default=0, max_digits=10, decimal_places=2)

    def deposit(self, amount):
        with transaction.atomic():
            self.balance += amount
            self.save()

    def withdraw(self, amount):
        with transaction.atomic():
            if self.balance >= amount:
                self.balance -= amount
                self.save()
                return True
        return False


class Transaction(models.Model):
    sender = models.ForeignKey(Account, related_name='sent_transactions', on_delete=models.CASCADE)
    receiver = models.ForeignKey(Account, related_name='received_transactions', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    @classmethod
    def create_transaction(cls, sender, receiver, amount):
        with transaction.atomic():
            if sender.withdraw(amount):
                receiver.deposit(amount)
                return cls.objects.create(sender=sender, receiver=receiver, amount=amount)
        return None