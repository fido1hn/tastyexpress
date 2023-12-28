from django.urls import path
from django.contrib.auth import views as auth_view

from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path("sign-in/", auth_view.LoginView.as_view(template_name="core/sign-in.html"), name="sign-in"),
    path("sign-out/", auth_view.LogoutView.as_view(next_page="/"), name="sign-out"),
    path("sign-up/", views.sign_up, name="sign-up"),

    path('customer/', views.customer_page, name='customer'),
    path('courier/', views.courier_page, name='courier'),
]
