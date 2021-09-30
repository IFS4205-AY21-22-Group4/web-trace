from django.http import HttpResponse
from django.shortcuts import redirect


def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_verified:
            return redirect("home")
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func


def verified_user(view_func):
    def wrapper_function(request, *args, **kwargs):
        user = request.user
        if user.is_authenticated and user.is_verified:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponse("You are not authorized to view this page")

    return wrapper_function


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


def admin_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name

        if group == "Administrators":
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponse("You are not authorized to view this page")

    return wrapper_function


def official_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name

        if group == "Officials":
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponse("You are not authorized to view this page")

    return wrapper_function


def tracer_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name

        if group == "Contact Tracers":
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponse("You are not authorized to view this page")

    return wrapper_function


def issuer_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name

        if group == "Token Issuers":
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponse("You are not authorized to view this page")

    return wrapper_function
