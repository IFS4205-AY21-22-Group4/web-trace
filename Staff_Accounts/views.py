from Staff_Accounts.models import CustomUser
from Staff_Accounts.decorator import admin_only, unauthenticated_user
from django.contrib.auth.models import Group
from django.http.response import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404, Http404
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import CreateUserForm
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from Staff_Accounts.activate import helpers
from django.core.mail import EmailMessage

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
            # send email verification now
            activation_key = helpers.generate_activation_key(
                username=request.POST["username"]
            )

            subject = "Central Login Account Verification"

            message = """\n
            Please visit the following link to verify your account \n\n{0}://{1}/activate/account/?key={2}
                                    """.format(
                request.scheme, request.get_host(), activation_key
            )

            error = False
            try:
                send_mail(
                    subject, message, settings.SERVER_EMAIL, [request.POST["email"]]
                )
                messages.add_message(
                    request,
                    messages.INFO,
                    "Account created! Click on the link sent to your email to activate the account",
                )

            except:
                error = True
                messages.add_message(
                    request,
                    messages.INFO,
                    "Unable to send email verification. Please try again",
                )
                context = {"form": form}
                return render(request, "accounts/register.html", context)

            user.activation_key = activation_key
            user.is_active = False
            user = form.cleaned_data.get("username")
            messages.success(request, "Account was created for " + user)

            form.save()

            return redirect("register")

    context = {"form": form}
    return render(request, "accounts/register.html", context)


@unauthenticated_user
def activate_account(request):
    key = request.GET["key"]
    if not key:
        raise Http404()

    user = get_object_or_404(CustomUser, activation_key=key, email_validated=False)
    user.is_active = True
    user.save()
    user.email_validated = True
    user.save()

    return render(request, "accounts/activated.html")


@unauthenticated_user
def loginPage(request):
    if request.user.is_authenticated:
        return redirect("home")
    else:
        if request.method == "POST":
            username = request.POST.get("username")
            password = request.POST.get("password")

            user = authenticate(request, username=username, password=password)

            if user.is_active == False:
                messages.info(
                    request,
                    "Please Activate your account using your email before login",
                )
            elif user is not None:
                login(request, user)
                return redirect("home")
            else:
                messages.info(request, "Username or Password is incorrect")

        context = {}
        return render(request, "accounts/login.html", context)


@login_required(login_url="login")
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
        return redirect("logout")
