from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model


# Create your models here.
class Plan(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_months = models.PositiveIntegerField(default=1)  # tambah ini

    def __str__(self):
        return self.name


def get_duration_months(self):
    if self.status == "paid":
        delta = timezone.now() - self.created_at
        return round(delta.total_seconds() / (30 * 24 * 60 * 60), 2)
    return 0.0


class Invoice(models.Model):
    STATUS_CHOICES = [
        ("paid", "Paid"),
        ("pending", "Pending"),
        ("failed", "Failed"),
    ]
    PAYMENT_METHOD_CHOICES = [
        ("card", "Card"),
        ("e-wallet", "E-wallet"),
        ("bank-transfer", "Bank Transfer"),
        ("other", "Other"),
    ]
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    plan = models.ForeignKey("Plan", on_delete=models.SET_NULL, null=True)
    billing_period_start = models.DateField()
    billing_period_end = models.DateField()
    amount_charged = models.DecimalField(max_digits=10, decimal_places=2)
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    auto_renewal = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    def total_due(self):
        return self.amount_charged + self.tax - self.discount

    def __str__(self):
        return f"Invoice {self.id} - {self.user.username} - {self.status}"
