from Staff_Accounts.decorator import admin_only, unauthenticated_user
from django.contrib.auth.models import Group
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import CreateUserForm
from django.contrib.auth.decorators import login_required


# Create your views here.
@admin_only
def registerPage(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            role = request.POST["roles"]
            if role.lower() == "administrators":
                user = form.save()
                user.is_staff = True
                group = Group.objects.get(name="Administrators")
                user.groups.add(group)
            elif role.lower() == "officials":
                user = form.save()
                group = Group.objects.get(name="Officials")
                user.groups.add(group)
            elif role.lower() == "contact tracers":
                user = form.save()
                group = Group.objects.get(name="Contact Tracers")
                user.groups.add(group)
            elif role.lower() == "token issuers":
                user = form.save()
                group = Group.objects.get(name="Token Issuers")
                user.groups.add(group)
            else:
                messages.add_message(
                    request,
                    messages.INFO,
                    "Invalid Role! Please choose among Administrators, Officials, Contact Tracers & Token Issuers",
                )
                context = {"form": form}
                return render(request, "accounts/register.html", context)

            form.save()
            user = form.cleaned_data.get("username")
            messages.success(request, "Account was created for " + user)

            return redirect("home")

    context = {"form": form}
    return render(request, "accounts/register.html", context)


@unauthenticated_user
def loginPage(request):
    if request.user.is_authenticated:
        return redirect("home")
    else:
        if request.method == "POST":
            username = request.POST.get("username")
            password = request.POST.get("password")

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect("home")
            else:
                messages.info(request, "Username or Password is incorrect")

        context = {}
        return render(request, "accounts/login.html", context)


def logoutUser(request):
    logout(request)
    return redirect("login")


@login_required(login_url="login")
def home(request):
    group = None
    if request.user.groups.exists():
        group = request.user.groups.all()[0].name
    if group == "Administrators":
        return render(request, "accounts/admin.html")
    elif group == "Officials":
        return render(request, "accounts/official.html")
    elif group == "Contact Tracers":
        return render(request, "accounts/tracer.html")
    elif group == "Token Issuers":
        return render(request, "accounts/issuer.html")
    else:
        logoutUser()
