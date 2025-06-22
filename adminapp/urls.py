# # adminapp/urls.py
from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.admin_dashboard, name='admin_dashboard'),
    path("dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("subscriptions/", views.subscription_list, name="subscription_list"),
    path("users/", views.user_list, name="user_list"),
    path("dashboard/report/", views.billing_report, name="billing_report"),
    path("logout/", LogoutView.as_view(next_page="login"), name="logout"),
    path("billing/", views.billing_list, name="billing_list"),
    path("billing/export_csv/", views.export_invoices_csv, name="export_invoices_csv"),
    path("billing/<int:invoice_id>/", views.invoice_detail, name="invoice_detail"),
    path(
        "billing/failed/", views.failed_payments_monitor, name="failed_payments_monitor"
    ),
]

# from django.urls import path
# from . import views

# urlpatterns = [
#     path('dashboard/', views.dashboard_view, name='admin_dashboard'),

#     # path('subscriptions/', views.subscription_list, name='admin_subscription_list'),
# ]
