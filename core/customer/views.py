from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.conf import settings

import stripe
import firebase_admin
from firebase_admin import credentials, auth

from . import forms


cred = credentials.Certificate(settings.FIREBASE_ADMIN_CREDENTIALS)
firebase_admin.initialize_app(cred)
stripe.api_key = settings.STRIPE_API_SECRET_KEY


@login_required()
def home(request):
    return redirect("customer:profile")


@login_required(login_url="/sign-in/?next=/customer/")
def profile_page(request):
    user_form = forms.BasicUserForm(instance=request.user)
    customer_form = forms.BasicCustomerForm(instance=request.user.customer)
    password_form = PasswordChangeForm(request.user)

    if request.method == "POST":

        if request.POST.get("action") == "update_profile":
            user_form = forms.BasicUserForm(
                request.POST, instance=request.user)
            customer_form = forms.BasicCustomerForm(
                request.POST, request.FILES, instance=request.user.customer)

            if user_form.is_valid() and customer_form.is_valid():
                user_form.save()
                customer_form.save()
                messages.success(request, "Your profile updated successfully.")
                return redirect("customer:profile")

        elif request.POST.get("action") == "update_password":
            password_form = PasswordChangeForm(request.user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(
                    request, "Your password updated successfully.")
                return redirect("customer:profile")

        elif request.POST.get("action") == "update_phone":
            # Get firebase user data
            firebase_user = auth.verify_id_token(request.POST.get("id_token"))
            request.user.customer.phone_number = firebase_user["phone_number"]
            request.user.customer.save()
            return redirect("customer:profile")

    return render(request, "core/customer/profile.html", {
        "user_form": user_form,
        "customer_form": customer_form,
        "password_form": password_form,
    })


@login_required(login_url="/sign-in/?next=/customer/")
def payment_method_page(request):
    current_customer = request.user.customer
    # Save stripe customer info
    if not current_customer.stripe_customer_id:
        customer = stripe.Customer.create()
        current_customer.stripe_customer_id = customer['id']
        current_customer.save()

    intent = stripe.SetupIntent.create(
        customer=current_customer.stripe_customer_id
    )
    return render(request, "core/customer/payment_method.html", {
        "client_secret": intent.client_secret,
        "STRIPE_API_PUBLIC_KEY": settings.STRIPE_API_PUBLIC_KEY,
    })
