from rest_framework import serializers
from .models import Transaction

class TransactionSerializer(serializers.ModelSerializer):
    balance_after_transaction = serializers.FloatField(required = False)
    class Meta:
        model = Transaction
        fields = ['transaction_type', 'amount', 'balance_after_transaction']