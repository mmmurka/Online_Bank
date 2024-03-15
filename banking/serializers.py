from rest_framework import serializers
from .models import Account, Transaction

"""
Сериализаторы для модели Account и Transaction
"""


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['sender', 'receiver', 'amount', 'timestamp']