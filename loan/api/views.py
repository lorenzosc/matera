from rest_framework.response import Response
from rest_framework import viewsets, mixins, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
import numpy as np
from .models import Loan, Payment
from .serializers import LoanSerializer, PaymentSerializer
from django.utils import timezone

class LoanViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin
):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Loan.objects.filter(user=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        loan = self.get_object()
        payments = Payment.objects.filter(loan=loan).order_by('date')

        if loan.user != request.user:
            raise PermissionDenied("You do not have permission to access this loan.")

        pro_rata_day = loan.interest_rate / 30 / 100
        still_due = loan.value
        last_day = loan.request_date

        for payment in payments:
            date_diff = (payment.date - last_day).days
            interest = still_due * np.power(1 + pro_rata_day, date_diff)
            still_due = round(interest - payment.value, 2)
            last_day = payment.date

        if still_due > 0:
            interest = still_due * np.power(1 + pro_rata_day, (timezone.now() - last_day).days)
            still_due = round(interest, 2)

        loan_data = LoanSerializer(loan).data
        payments_data = PaymentSerializer(payments, many=True).data
        loan_data['still_due'] = still_due

        return Response({
            'loan': loan_data,
            'payments': payments_data
        }, status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class PaymentViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin
):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        loan = serializer.validated_data.get('loan')

        if loan.user != self.request.user:
            raise PermissionDenied(
                """
                You are not allowed to create
                payments for loans you do not own.
                """
            )

        serializer.save(user=self.request.user)
