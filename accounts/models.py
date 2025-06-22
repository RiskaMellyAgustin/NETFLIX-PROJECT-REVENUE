from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ("admin", "Admin"),
        ("user", "User"),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="user")

    def __str__(self):
        return self.username


# class Plan(models.Model):
#     name = models.CharField(max_length=100)
#     price = models.DecimalField(max_digits=10, decimal_places=0)

#     def __str__(self):
#         return self.name

# class Subscription(models.Model):
#     STATUS_CHOICES = [
#         ('pending', 'Pending'),
#         ('paid', 'Paid'),
#         ('expired', 'Expired'),
#     ]

#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     plan = models.ForeignKey(Plan, on_delete=models.SET_NULL, null=True)
#     start_date = models.DateTimeField(auto_now_add=True)
#     status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
#     payment_method = models.CharField(max_length=50)
#     notes = models.TextField(blank=True, null=True)

#     def __str__(self):
#         return f"{self.user.username} - {self.plan.name} - {self.status}"
