# customerapp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("subscribe/", views.subscribe_page, name="subscribe_page"),
    path("subscribe/success/", views.subscribe_success, name="subscribe_success"),
    path(
        "subscribe/invoice/<int:subscription_id>/",
        views.subscription_invoice,
        name="subscription_invoice",
    ),
    path(
        "subscribe/mark-paid/<int:subscription_id>/",
        views.mark_as_paid,
        name="mark_as_paid",
    ),
]
# urlpatterns = [
#     path('subscribe/', views.subscribe_page, name='subscribe_page'),
#     path('subscribe/success/', views.subscribe_success, name='subscribe_success'),
# ]
