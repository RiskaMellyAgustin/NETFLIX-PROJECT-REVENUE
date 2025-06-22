from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import CustomUser  # Import model custom kamu
from django.contrib.auth import get_user_model
from .forms import CustomUserCreationForm  # <-- kuning kalau belum dipakai


User = get_user_model()  # pakai CustomUser


@login_required
def subscribe_page(request):
    # Jika Anda memiliki model Plan, uncomment ini
    # plans = Plan.objects.all()

    if request.method == "POST":
        # Logika untuk menangani subscription
        # selected_plan_id = request.POST.get('plan')
        # payment_method = request.POST.get('payment_method')
        # notes = request.POST.get('notes')

        # plan = Plan.objects.get(id=selected_plan_id)

        # Subscription.objects.create(
        #     user=request.user,
        #     plan=plan,
        #     status='pending',
        #     payment_method=payment_method,
        #     notes=notes
        # )

        return redirect("subscription_success")

    return render(request, "customerapp/subscribe_page.html")  # , {'plans': plans}


def landing_page(request):
    return render(request, "accounts/index.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Cek role user
            if user.is_superuser:
                return redirect("admin_dashboard")  # URL adminapp
            else:
                return redirect("customer_dash")  # URL customerapp
        else:
            messages.error(request, "Invalid username or password")
    return render(request, "accounts/login.html")


# def login_view(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')

#         user = authenticate(request, username=username, password=password)

#         if user is not None:
#             login(request, user)
#             if user.role == 'admin':
#                 return redirect('admin_dashboard')  # ganti sesuai url name kamu
#             else:
#                 return redirect('customer_dash')  # ganti sesuai url name kamu
#         else:
#             messages.error(request, "Username atau password salah.")
#             return redirect('customer_dash')
#     return render(request, 'accounts/login.html')


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # <- Login langsung setelah register
            return redirect("customer_dash")  # <- Redirect ke customer page
    else:
        form = CustomUserCreationForm()
    return render(request, "accounts/register.html", {"form": form})


# @login_required
# def subscribe_page(request):
#     plans = Plan.objects.all()

#     if request.method == 'POST':
#         selected_plan_id = request.POST.get('plan')
#         payment_method = request.POST.get('payment_method')
#         notes = request.POST.get('notes')

#         plan = Plan.objects.get(id=selected_plan_id)

#         Subscription.objects.create(
#             user=request.user,
#             plan=plan,
#             status='pending',
#             payment_method=payment_method,
#             notes=notes
#         )

#         return redirect('subscription_success')

#     return render(request, 'accounts/subscribe_page.html', {'plans': plans})


@login_required
def subscribe_success(request):
    return render(request, "accounts/subscribe_success.html")


# def register(request):
#     if request.method == 'POST':
#         form = CustomUserCreationForm(request.POST)
#         if form.is_valid():
#             form.save()  # <-- INI PENTING
#             return redirect('index')
#     else:
#         form = CustomUserCreationForm()
#     return render(request, 'accounts/register.html', {'form': form})


def customer_dash(request):
    return render(request, "accounts/customer_dash.html")


def logout_view(request):
    logout(request)
    return redirect("index")
