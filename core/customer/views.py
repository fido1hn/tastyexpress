from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from . import forms


@login_required()
def home(request):
    return redirect("customer:profile")


@login_required(login_url="/sign-in/?next=/customer/")
def profile_page(request):
    user_form = forms.BasicUserForm(instance=request.user)
    if request.method == "POST":
        user_form = forms.BasicUserForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            return redirect("customer:profile")
    return render(request, "core/customer/profile.html", {
        "user_form": user_form,
    })
