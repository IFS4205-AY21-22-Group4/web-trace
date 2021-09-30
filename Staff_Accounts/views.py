from Staff_Accounts.models import CustomUser
from Staff_Accounts.helpers.wrappers import (
    admin_only,
    unauthenticated_user,
    verified_user,
)

from django.shortcuts import render, redirect, get_object_or_404, Http404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from Staff_Accounts.helpers.forms import CreateUserForm, CreateUserOTPForm
from django.contrib.auth.decorators import login_required
from Staff_Accounts.helpers import crypto
from Staff_Accounts.helpers.validate import (
    sendOTP,
    validateRoles,
    sendVerificationEmail,
)

# Create your views here.
@admin_only
@verified_user
def registerPage(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            # Roles Verification
            role = request.POST["roles"]
            group_error = validateRoles(form, role)
            if group_error:
                messages.add_message(
                    request,
                    messages.INFO,
                    "Invalid Role! Please choose among Administrators, Officials, Contact Tracers & Token Issuers",
                )
                context = {"form": form}
                return render(request, "accounts/register.html", context)

            # Email verification
            activation_key = crypto.generate_activation_key(
                username=request.POST["username"]
            )
            email_verification_error = sendVerificationEmail(request, activation_key)

            if email_verification_error:
                messages.add_message(
                    request,
                    messages.INFO,
                    "Unable to send email verification. Please try again",
                )
                context = {"form": form}
                return render(request, "accounts/register.html", context)

            user = form.save()
            user.activation_key = activation_key
            user = form.cleaned_data.get("username")
            messages.success(request, "Account was created for " + user)

            form.save()
            return redirect("register")  # Sends a new form

    context = {"form": form}
    return render(request, "accounts/register.html", context)


@unauthenticated_user
def activate_account(request):
    key = request.GET["key"]
    if not key:
        raise Http404()

    user = get_object_or_404(CustomUser, activation_key=key, email_validated=False)
    user.email_validated = True
    user.save()

    return render(request, "accounts/activated.html")


@unauthenticated_user
def loginPage(request):

    if request.user.is_authenticated:
        if request.user.is_verified:
            return redirect("home")
        logoutUser(request)
    else:
        if request.method == "POST":
            username = request.POST.get("username")
            password = request.POST.get("password")

            user = authenticate(request, username=username, password=password)

            if user is not None:
                if (
                    user.email_validated == False
                ):  # User need to activate email address first
                    messages.info(
                        request,
                        "Please Activate your account using your email before login",
                    )
                else:
                    login(request, user)

                    new_otp = crypto.generate_otp()
                    otp_verification_error = sendOTP(request, new_otp, user)

                    if otp_verification_error:
                        messages.add_message(
                            request,
                            messages.INFO,
                            "Unable to send otp verification. Please try again",
                        )
                        logoutUser(
                            request
                        )  # logout user for the time being if OTP cannot be sent
                        context = {}
                        return render(request, "accounts/login.html", context)

                    user.most_recent_otp = new_otp
                    user.save()
                    return redirect("otp")

            else:
                messages.info(request, "Username or Password is incorrect")

    context = {}
    return render(request, "accounts/login.html", context)


@login_required(login_url="login")
def logoutUser(request):
    user = request.user
    user.is_verified = False
    user.save()
    logout(request)
    return redirect("login")


@verified_user
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


@login_required(login_url="login")
def otpVerification(request):
    form = CreateUserOTPForm
    if request.method == "POST":
        form = CreateUserOTPForm(request.POST)
        user = request.user
        otp = request.POST["otp"]
        if otp == user.most_recent_otp:
            user.is_verified = True
            user.save()
            return redirect("home")
        else:
            messages.error(request, "Invalid OTP")

    context = {"form": form}
    return render(request, "accounts/otp.html", context)
