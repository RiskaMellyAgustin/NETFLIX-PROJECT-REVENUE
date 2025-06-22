# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = "customer"  # Force jadi customer
        if commit:
            user.save()
        return user


# from django import forms
# from django.contrib.auth.forms import UserCreationForm
# from .models import CustomUser

# class CustomUserCreationForm(UserCreationForm):
#     class Meta:
#         model = CustomUser
#         fields = ['username', 'email', 'password1', 'password2', 'role']
