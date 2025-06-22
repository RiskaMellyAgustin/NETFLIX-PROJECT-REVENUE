from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Plan, Subscription
from django.db import IntegrityError
from datetime import date, timedelta
from decimal import Decimal
from django.contrib import messages


@login_required
def subscribe_page(request):
    plans = Plan.objects.all().distinct()

    # Daftar pilihan payment_method valid (harus sama seperti di models)
    valid_payment_methods = [
        choice[0] for choice in Subscription.PAYMENT_METHOD_CHOICES
    ]
    valid_durations = ["month", "year"]

    if request.method == "POST":
        plan_id = request.POST.get("plan_id")
        duration = request.POST.get("duration")
        payment_method = request.POST.get("payment_method")

        # Validasi input
        if not plan_id or not duration or not payment_method:
            messages.error(request, "All fields must be filled.")
            return render(request, "customerapp/subscribe_page.html", {"plans": plans})

        if duration not in valid_durations:
            messages.error(request, "Invalid subscription duration.")
            return render(request, "customerapp/subscribe_page.html", {"plans": plans})

        if payment_method not in valid_payment_methods:
            messages.error(request, "Invalid payment method.")
            return render(request, "customerapp/subscribe_page.html", {"plans": plans})

        plan = get_object_or_404(Plan, id=plan_id)

        start_date = date.today()

        if duration == "month":
            end_date = start_date + timedelta(days=30)
            total_price = plan.price
        else:  # year
            end_date = start_date + timedelta(days=365)
            total_price = plan.price * 12 * Decimal("0.9")  # diskon 10%

        try:
            subscription = Subscription.objects.create(
                user=request.user,
                plan=plan,
                payment_method=payment_method,
                status="unpaid",
                start_date=start_date,
                end_date=end_date,
                total_price=total_price,
                # order_id tidak perlu diisi manual karena sudah otomatis di save()
            )
            return redirect("subscription_invoice", subscription_id=subscription.id)
        except IntegrityError:
            messages.error(
                request,
                "An error occurred while creating a subscription. Please try again.",
            )
            return render(request, "customerapp/subscribe_page.html", {"plans": plans})

    return render(request, "customerapp/subscribe_page.html", {"plans": plans})


@login_required
def subscription_invoice(request, subscription_id):
    subscription = get_object_or_404(
        Subscription, id=subscription_id, user=request.user
    )
    return render(
        request, "customerapp/subscription_invoice.html", {"subscription": subscription}
    )


@login_required
def mark_as_paid(request, subscription_id):
    subscription = get_object_or_404(
        Subscription, id=subscription_id, user=request.user
    )
    subscription.status = "paid"
    subscription.save()

    request.session["subscription_id"] = subscription.id

    return redirect("subscribe_success")


@login_required
def subscribe_success(request):
    subscription_id = request.session.get("subscription_id")

    if not subscription_id:
        return render(
            request,
            "customerapp/subscribe_success.html",
            {"error": "Subscription not found."},
        )

    subscription = get_object_or_404(
        Subscription, id=subscription_id, user=request.user
    )

    return render(
        request, "customerapp/subscribe_success.html", {"subscription": subscription}
    )
