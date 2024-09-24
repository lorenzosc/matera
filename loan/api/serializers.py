from rest_framework import serializers
from .models import Loan, Payment

class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        exclude = ['user', 'id']

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        exclude = ['user']
