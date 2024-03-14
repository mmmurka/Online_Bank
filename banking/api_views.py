from rest_framework import viewsets
from .models import Account, Transaction
from .serializers import AccountSerializer, TransactionSerializer


class AccountListCreateAPIView(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


class TransactionListCreateAPIView(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
