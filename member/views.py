from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.urls import reverse
from .forms import CustomUserCreationForm


def dashboard(request):
    return render(request, "member/dashboard.html")


def register(request):
    if request.method == "GET":
        return render(
            request, "member/register.html",
            {"form": CustomUserCreationForm}
        )
    elif request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(reverse("dashboard"))
