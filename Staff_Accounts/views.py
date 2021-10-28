from django.contrib.auth.models import User
import Staff_Accounts
from Staff_Accounts.models import Staff
from Staff_Accounts.helpers.wrappers import (
    admin_only,
    unauthenticated_user,
    unverified_user,
    verified_user,
)

from django.shortcuts import render, redirect, get_object_or_404, Http404
from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from Staff_Accounts.helpers.forms import (
    CreateUserForm,
    CreateUserOTPForm,
)
from django.contrib.auth.decorators import login_required
from Staff_Accounts.helpers import crypto
from Staff_Accounts.helpers.validate import (
    sendOTP,
    validateRoles,
    sendVerificationEmail,
)

import logging

from config.settings import DB

db_logger = logging.getLogger(DB)

# Create your views here.
@admin_only
@verified_user
def registerPage(request):
    form = CreateUserForm()
    db_logger.info("Register Page")
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            # Roles Verification
            user = form.save()
            role = request.POST["roles"]
            group_error = validateRoles(user, role)
            if group_error:
                user.delete()  # Delete created user
                messages.add_message(
                    request,
                    messages.INFO,
                    "Invalid Role! Please choose among Administrators, Officials, Contact Tracers & Token Issuers",
                )
                context = {"form": form}
                return render(request, "accounts/register.html", context)

            # Email verification
            email = request.POST["email"]
            activation_key = crypto.generate_activation_key(
                email=request.POST["email"]
            )  # form.cleaned_data.get("email")
            email_verification_error = sendVerificationEmail(
                request, activation_key, email
            )

            if email_verification_error:
                user.delete()  # Delete created user
                messages.add_message(
                    request,
                    messages.INFO,
                    "Unable to send email verification. Please try again",
                )
                context = {"form": form}
                return render(request, "accounts/register.html", context)

            Staff.objects.create(
                user=user,
                roles=role,
                activation_key=activation_key,
            )
            user.save()
            user = form.cleaned_data.get("email")
            db_logger.info("User created")
            messages.success(request, "Account was created for " + user)

            return redirect("register")  # Sends a new form

    context = {"form": form}
    return render(request, "accounts/register.html", context)


@unauthenticated_user
def activate_account(request):
    key = request.GET["key"]
    if not key:
        raise Http404()
    user = get_object_or_404(
        Staff, activation_key=key, email_validated=False
    )  # Cant be used multiple times
    db_logger.info("activate_account")
    user.email_validated = True
    user.save()

    return render(request, "accounts/activated.html")


@unauthenticated_user
def loginPage(request):
    db_logger.info("login")

    if request.user.is_authenticated:
        new_session_user = Staff.objects.get(user=request.user)
        if new_session_user.is_verified:
            return redirect("home")
        logoutUser(request)
    else:
        if request.method == "POST":
            email = request.POST.get("email")
            password = request.POST.get("password")

            authenticated_user = authenticate(request, email=email, password=password)
            try:
                new_session_user = Staff.objects.get(user=authenticated_user)
            except:
                new_session_user = None

            if new_session_user is not None:
                if (
                    new_session_user.email_validated == False
                ):  # User need to activate email address first
                    messages.info(
                        request,
                        "Please Activate your account using your email before login",
                    )
                else:
                    login(request, authenticated_user)

                    new_otp = crypto.generate_otp()
                    otp_verification_error = sendOTP(request, new_otp, email)

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

                    new_session_user.most_recent_otp = new_otp
                    new_session_user.save()
                    return redirect("otp")

            else:
                messages.info(request, "Email Address or Password is incorrect")

    context = {}
    return render(request, "accounts/login.html", context)


@verified_user
def logoutUser(request):
    db_logger.info("logout")

    user = get_object_or_404(Staff, user=request.user)
    user.is_verified = False
    user.save()
    logout(request)
    return redirect("login")


@verified_user
def home(request):
    db_logger.info("home")

    group = None
    if request.user.groups.exists():
        group = request.user.groups.all()[0].name
    if group == "Administrators":
        return render(request, "accounts/admin.html")
    elif group == "Officials":
        return render(request, "accounts/official.html")
    elif group == "Contact Tracers":
        return render(request, "tracer/tracer.html")
    elif group == "Token Issuers":
        return render(request, "issuer/index.html")
    else:
        logout(request)
        return redirect("login")


# add unverified
@login_required(login_url="login")
@unverified_user
def otp_verification(request):
    db_logger.info("otp_verification")

    form = CreateUserOTPForm
    if request.method == "POST":
        form = CreateUserOTPForm(request.POST)
        if form.is_valid:
            user = get_object_or_404(Staff, user=request.user)
            otp = request.POST["otp"]
            if user.number_of_attempts >= 2:  # 3 attempts in total
                user.email_validated = False
                activation_key = crypto.generate_activation_key(
                    email=request.user.email
                )
                email_verification_error = sendVerificationEmail(
                    request, activation_key, request.user.email
                )
                user.activation_key = activation_key
                user.number_of_attempts = 0
                user.save()
                logoutUser(request)
                messages.error(
                    request,
                    "Your account has been blocked. Please re-activate your account using your email before proceeding! If you didn't receive any mails, please reach out to an administrator",
                )
                return redirect("login")
            elif otp == user.most_recent_otp:
                user.is_verified = True
                user.number_of_attempts = 0
                user.save()
                return redirect("home")
            else:
                user.number_of_attempts = user.number_of_attempts + 1
                user.save()
                messages.error(request, "Invalid OTP")

    context = {"form": form}
    return render(request, "accounts/otp.html", context)
