from django.db import models
from django.contrib.auth.models import User
import uuid

class Loan(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    value = models.FloatField()
    interest_rate = models.FloatField()
    ip_address = models.GenericIPAddressField()
    request_date = models.DateTimeField(auto_now_add=True)
    bank = models.CharField(max_length=100)
    client = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Payment(models.Model):
    date = models.DateTimeField()
    value = models.FloatField()
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
