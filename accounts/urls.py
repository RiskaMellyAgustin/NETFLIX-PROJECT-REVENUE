from django.urls import path
from . import views

urlpatterns = [
    # Halaman utama (landing)
    path("", views.landing_page, name="index"),
    # Autentikasi
    path("login/", views.login_view, name="login"),
    path("register/", views.register, name="register"),
    path("logout/", views.logout_view, name="logout"),
    # Dashboard Customer
    path("customer_page/", views.customer_dash, name="customer_dash"),
    # path('subscribe/', views.subscribe_page, name='subscribe_page'),
    # path('subscribe/success/', views.subscribe_success, name='subscription_success'),
]

# urlpatterns = [
#     # path('', views.landing, name='landing'),
#     path('', views.landing_page, name='index'),
#     path('login/', views.login_view, name='login'),
#     path('register/', views.register, name='register'),
#     path('customer_page/', views.customer_dash, name='register'),
#     path('logout/', views.logout_view, name='logout'),
# ]
