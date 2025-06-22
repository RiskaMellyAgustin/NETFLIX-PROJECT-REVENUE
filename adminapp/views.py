from django.db.models import Sum, Count
from django.contrib.auth import get_user_model
from django.utils.timezone import now
from django.db.models.functions import TruncMonth
from customerapp.models import Subscription
import calendar

from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Count
from django.utils.timezone import now
from datetime import timedelta
from django.db.models import Q
from django.utils.timezone import now
from datetime import datetime, timedelta
from django.utils import timezone
from dateutil.relativedelta import relativedelta

from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, get_object_or_404
from .models import Invoice
from django.db.models import Q
from django.http import HttpResponse
import csv
from datetime import datetime


from django.db.models import Sum, Count, Q
from django.contrib.auth import get_user_model
from django.utils.timezone import now
from django.db.models.functions import TruncMonth
from customerapp.models import Subscription
from datetime import timedelta, datetime
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse
import csv
import calendar

from .models import Invoice

def admin_dashboard(request):
    return render(request, 'adminapp/dashboard.html')  


# Decorator untuk memastikan hanya admin (is_staff) yang bisa akses
def admin_required(view_func):
    return user_passes_test(lambda u: u.is_staff)(view_func)


@admin_required
def admin_dashboard(request):
    User = get_user_model()

    # Total revenue dari subscription yang sudah dibayar
    total_revenue = (
        Subscription.objects.filter(status="paid").aggregate(Sum("total_price"))[
            "total_price__sum"
        ]
        or 0
    )

    # Revenue yang belum dibayar
    unpaid_revenue = (
        Subscription.objects.filter(status="unpaid").aggregate(Sum("total_price"))[
            "total_price__sum"
        ]
        or 0
    )

    # Total user terdaftar (hanya customer)
    total_users = User.objects.filter(is_staff=False).count()

    # User yang punya subscription (aktif), hanya customer
    active_users = (
        Subscription.objects.filter(user__is_staff=False)
        .values("user")
        .distinct()
        .count()
    )

    # Customer yang belum pernah subscribe
    inactive_users = max(0, total_users - active_users)

    # Rasio pembayaran
    paid_count = Subscription.objects.filter(status="paid").count()
    unpaid_count = Subscription.objects.filter(status="unpaid").count()
    total_count = paid_count + unpaid_count
    payment_ratio = (paid_count / total_count * 100) if total_count > 0 else 0

    # Grafik revenue bulanan - 6 bulan terakhir
    six_months_ago = now() - timedelta(days=30 * 6)
    monthly_revenue = (
        Subscription.objects.filter(status="paid", created_at__gte=six_months_ago)
        .annotate(month=TruncMonth("created_at"))
        .values("month")
        .annotate(total=Sum("total_price"))
        .order_by("month")
    )

    chart_data = {
        "labels": [calendar.month_name[m["month"].month] for m in monthly_revenue],
        "data": [float(m["total"]) for m in monthly_revenue],
    }

    # 5 subscription terbaru
    recent_subscriptions = Subscription.objects.select_related("user", "plan").order_by(
        "-created_at"
    )[:5]

    context = {
        "total_revenue": total_revenue,
        "unpaid_revenue": unpaid_revenue,
        "total_users": total_users,
        "active_users": active_users,
        "inactive_users": inactive_users,
        "payment_ratio": payment_ratio,
        "chart_data": chart_data,
        "recent_subscriptions": recent_subscriptions,
    }

    return render(request, "adminapp/dashboard.html", context)


@admin_required
def billing_report(request):
    # Filter by date
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")

    transactions = Subscription.objects.all()

    if start_date:
        transactions = transactions.filter(created_at__gte=start_date)
    if end_date:
        transactions = transactions.filter(created_at__lte=end_date)

    # Calculate metrics
    total_revenue = (
        transactions.filter(status="paid").aggregate(Sum("total_price"))[
            "total_price__sum"
        ]
        or 0
    )

    paid_count = transactions.filter(status="paid").count()
    unpaid_count = transactions.filter(status="unpaid").count()

    six_months_ago = now() - timedelta(days=30 * 6)

    # Ambil data bulanan total_price untuk subscription yang dibayar dalam 6 bulan terakhir
    monthly_revenue = (
        Subscription.objects.filter(
            created_at__gte=six_months_ago,
            status="paid",
        )
        .annotate(month=TruncMonth("created_at"))
        .values("month")
        .annotate(total=Sum("total_price"))
        .order_by("month")
    )

    chart_labels = [calendar.month_name[m["month"].month] for m in monthly_revenue]
    chart_data = [float(m["total"]) for m in monthly_revenue]

    recent_transactions = transactions.order_by("-created_at")[:10]

    context = {
        "total_revenue": total_revenue,
        "paid_count": paid_count,
        "unpaid_count": unpaid_count,
        "arpu": total_revenue / paid_count if paid_count > 0 else 0,
        "recent_transactions": recent_transactions,
        "chart_labels": chart_labels,
        "chart_data": chart_data,
    }
    return render(request, "adminapp/report.html", context)


@admin_required
def subscription_list(request):
    subscriptions = (
        Subscription.objects.select_related("user", "plan")
        .filter(user__is_staff=False)  # hanya user biasa
        .order_by("-created_at")
    )

    active_count = Subscription.objects.filter(
        status="paid", user__is_staff=False
    ).count()
    inactive_count = Subscription.objects.filter(
        ~Q(status="paid"), user__is_staff=False
    ).count()

    plan_counts = (
        Subscription.objects.filter(user__is_staff=False, status="paid")
        .values("plan__name")
        .annotate(count=Count("id"))
    )

    now = timezone.now()
    for sub in subscriptions:
        if sub.status == "paid" and sub.created_at:
            delta = now - sub.created_at
            sub.active_months = round(
                delta.days / 30.44, 2
            )  # 30.44 = rata-rata hari per bulan
        else:
            sub.active_months = 0.0

    return render(
        request,
        "adminapp/subscription_list.html",
        {
            "subscriptions": subscriptions,
            "active_count": active_count,
            "inactive_count": inactive_count,
            "plan_counts": plan_counts,
        },
    )


@admin_required
def user_list(request):
    User = get_user_model()
    users = User.objects.filter(is_staff=False)  # hanya user biasa

    # Ambil subscription terbaru per user (user biasa saja)
    latest_subs = (
        Subscription.objects.select_related("plan", "user")
        .filter(user__is_staff=False)
        .order_by("user_id", "-created_at")
        .distinct("user_id")
    )

    user_subscriptions = {sub.user_id: sub for sub in latest_subs}

    return render(
        request,
        "adminapp/user_list.html",
        {
            "users": users,
            "user_subscriptions": user_subscriptions,
        },
    )


# # @admin_required
# def user_list(request):
#     User = get_user_model()
#     users = User.objects.all()

#     # Buat dictionary: user_id -> (plan_id, created_at)
#     user_subscriptions = {
#         sub.user_id: (sub.plan_id, sub.created_at)
#         for sub in Subscription.objects.order_by('user_id', '-created_at').distinct('user_id')
#     }

#     return render(request, 'adminapp/user_list.html', {
#         'users': users,
#         'user_subscriptions': user_subscriptions,
#     })


# adminapp/views.py
from django.db.models.functions import TruncMonth
import calendar


def billing_report(request):
    # Filter by date
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")

    transactions = Subscription.objects.all()

    if start_date:
        transactions = transactions.filter(created_at__gte=start_date)
    if end_date:
        transactions = transactions.filter(created_at__lte=end_date)

    # Calculate metrics
    total_revenue = (
        transactions.filter(status="paid").aggregate(Sum("total_price"))[
            "total_price__sum"
        ]
        or 0
    )

    paid_count = transactions.filter(status="paid").count()
    unpaid_count = transactions.filter(status="unpaid").count()

    six_months_ago = now() - timedelta(days=30 * 6)

    # Ambil data bulanan total_price untuk subscription yang dibayar dalam 6 bulan terakhir
    monthly_revenue = (
        Subscription.objects.filter(
            created_at__gte=six_months_ago,
            status="paid",
        )
        .annotate(month=TruncMonth("created_at"))
        .values("month")
        .annotate(total=Sum("total_price"))
        .order_by("month")
    )

    chart_labels = [calendar.month_name[m["month"].month] for m in monthly_revenue]
    chart_data = [float(m["total"]) for m in monthly_revenue]

    recent_transactions = transactions.order_by("-created_at")[:10]

    context = {
        "total_revenue": total_revenue,
        "paid_count": paid_count,
        "unpaid_count": unpaid_count,
        "arpu": total_revenue / paid_count if paid_count > 0 else 0,
        "recent_transactions": recent_transactions,
        "chart_labels": chart_labels,
        "chart_data": chart_data,
    }
    return render(request, "adminapp/report.html", context)


@admin_required
def billing_list(request):
    query = request.GET.get("q", "")
    status_filter = request.GET.get("status", "")
    payment_method_filter = request.GET.get("payment_method", "")

    subscriptions = Subscription.objects.select_related("user", "plan").all()

    if query:
        subscriptions = subscriptions.filter(
            Q(order_id__icontains=query) | Q(user__email__icontains=query)
        )

    if status_filter:
        subscriptions = subscriptions.filter(status=status_filter)

    if payment_method_filter:
        subscriptions = subscriptions.filter(payment_method=payment_method_filter)

    context = {
        "subscriptions": subscriptions,
    }
    return render(request, "adminapp/billing_list.html", context)


@admin_required
def invoice_detail(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    return render(request, "adminapp/invoice_detail.html", {"invoice": invoice})


@admin_required
def export_invoices_csv(request):
    # Export filtered invoices to CSV
    invoices = Invoice.objects.all().order_by("-created_at")

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = (
        f'attachment; filename="invoices_{datetime.now().strftime("%Y%m%d")}.csv"'
    )

    writer = csv.writer(response)
    writer.writerow(
        [
            "Invoice ID",
            "User",
            "Plan",
            "Billing Period",
            "Amount Charged",
            "Tax",
            "Discount",
            "Total Due",
            "Status",
            "Payment Method",
            "Auto Renewal",
            "Created At",
            "Updated At",
        ]
    )

    for inv in invoices:
        writer.writerow(
            [
                inv.id,
                inv.user.username,
                inv.plan.name if inv.plan else "",
                f"{inv.billing_period_start} - {inv.billing_period_end}",
                inv.amount_charged,
                inv.tax,
                inv.discount,
                inv.total_due(),
                inv.status,
                inv.payment_method,
                "Yes" if inv.auto_renewal else "No",
                inv.created_at,
                inv.updated_at,
            ]
        )

    return response


@admin_required
def failed_payments_monitor(request):
    failed_invoices = Invoice.objects.filter(status="failed").order_by("-updated_at")

    # Example simple retry or send reminder logic can be done here or via Celery background job

    context = {
        "failed_invoices": failed_invoices,
    }
    return render(request, "adminapp/failed_payments.html", context)
