from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from . import forms


@login_required()
def home(request):
    return redirect("customer:profile")


@login_required(login_url="/sign-in/?next=/customer/")
def profile_page(request):
    user_form = forms.BasicUserForm(instance=request.user)
    customer_form = forms.BasicCustomerForm(instance=request.user.customer)

    if request.method == "POST":
        user_form = forms.BasicUserForm(request.POST, instance=request.user)
        customer_form = forms.BasicCustomerForm(
            request.POST, request.FILES, instance=request.user.customer)

        if user_form.is_valid() and customer_form.is_valid():
            user_form.save()
            customer_form.save()

            messages.success(request, "Profile updated successfully.")
            return redirect("customer:profile")

    return render(request, "core/customer/profile.html", {
        "user_form": user_form,
        "customer_form": customer_form,
    })
