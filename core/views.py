from django.shortcuts import render, redirect
from django.contrib.auth import login

from .forms import SignUpForm


def home(request):
    return render(request, "core/home.html")


def sign_up(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email').lower()
            user = form.save(commit=False)
            user.username = email
            user.save()

            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect("home")
    return render(request, "core/sign-up.html", {'form': form})
