from django.db import models
from django.conf import settings
from datetime import datetime
from dateutil.relativedelta import relativedelta


class Plan(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name} - IDR {self.price}"


def generate_order_id():
    today = datetime.today().strftime("%Y%m%d")
    prefix = f"INV-{today}"
    # Hitung jumlah subscription yang sudah ada hari ini
    count_today = Subscription.objects.filter(order_id__startswith=prefix).count() + 1
    return f"{prefix}-{count_today:04d}"


class Subscription(models.Model):
    BILLING_PERIOD_CHOICES = [
        ("monthly", "Monthly"),
        ("yearly", "Yearly"),
    ]

    PAYMENT_METHOD_CHOICES = [
        ("credit", "Credit Card"),  # Diubah dari credit_card
        ("ewallet", "e-Wallet"),  # Ditambahkan
        ("bank_transfer", "Bank Transfer"),
        ("other", "Other"),
    ]

    STATUS_CHOICES = [
        ("unpaid", "Unpaid"),
        ("paid", "Paid"),
        ("cancelled", "Cancelled"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    total_price = models.DecimalField(max_digits=12, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="unpaid")
    order_id = models.CharField(max_length=30, unique=True, blank=True)  # auto-generate
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.order_id:
            self.order_id = generate_order_id()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.order_id} - {self.user.username} - {self.plan.name}"

    billing_period = models.CharField(
        max_length=10, choices=BILLING_PERIOD_CHOICES, default="monthly"
    )

    @property
    def active_duration(self):
        if not self.start_date or not self.end_date:
            return (0, 0)

        delta = relativedelta(self.end_date, self.start_date)
        months = delta.years * 12 + delta.months
        days = delta.days

        return (months, days)

    def get_active_duration_display(self):
        months, days = self.active_duration
        parts = []
        if months > 0:
            parts.append(f"{months} bulan")
        if days > 0:
            parts.append(f"{days} hari")
        if not parts:
            return "0 hari"
        return " ".join(parts)

    def clean(self):
        from django.core.exceptions import ValidationError

        if self.end_date <= self.start_date:
            raise ValidationError("End date harus lebih besar dari start date.")
