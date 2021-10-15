from django.contrib.auth import logout
from Staff_Accounts.models import Staff
from django.http import HttpResponse
from django.shortcuts import redirect

# Check if user is unauthenticated
def unauthenticated_user(view_func):
    def unauthenticated_wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            try:
                user = Staff.objects.get(user=request.user)
            except:
                return view_func(request, *args, **kwargs)
            if user.is_verified:
                return redirect("home")
            logout(request)
            return view_func(request, *args, **kwargs)
        else:
            return view_func(request, *args, **kwargs)

    return unauthenticated_wrapper_func


# Check if user has logged in with the OTP
def verified_user(view_func):
    def verified_wrapper_function(request, *args, **kwargs):
        if request.user.is_authenticated:
            try:
                user = Staff.objects.get(user=request.user)
            except:
                return HttpResponse("You are not authorized to view this page")
            if user.is_verified:
                return view_func(request, *args, **kwargs)
            return HttpResponse("You are not authorized to view this page")
        else:
            return HttpResponse("You are not authorized to view this page")

    return verified_wrapper_function


# Check if user has logged in without the OTP
def unverified_user(view_func):
    def wrapper_function(request, *args, **kwargs):
        if request.user.is_authenticated:
            try:
                user = Staff.objects.get(user=request.user)
            except:
                logout(request)
                redirect("login")
            if user.is_verified == False:
                return view_func(request, *args, **kwargs)
            else:
                return redirect("home")
        else:
            return HttpResponse("You are not authorized to view this page")

    return wrapper_function


# Check whether specified user is allowed to access view
def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):

            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name

            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse("You are not authorized to view this page")

        return wrapper_func

    return decorator


# Check whether user is admin
def admin_only(view_func):
    def admin_wrapper_function(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name

        if group == "Administrators":
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponse("You are not authorized to view this page")

    return admin_wrapper_function


# Check whether user is official
def official_only(view_func):
    def official_wrapper_function(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name

        if group == "Officials":
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponse("You are not authorized to view this page")

    return official_wrapper_function


# Check whether user is tracer
def tracer_only(view_func):
    def tracer_wrapper_function(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name

        if group == "Contact Tracers":
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponse("You are not authorized to view this page")

    return tracer_wrapper_function


# Check whether user is issuer
def issuer_only(view_func):
    def issuer_wrapper_function(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name

        if group == "Token Issuers":
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponse("You are not authorized to view this page")

    return issuer_wrapper_function
