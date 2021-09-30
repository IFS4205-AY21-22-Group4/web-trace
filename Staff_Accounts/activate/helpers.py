from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import hashlib
from django.utils.crypto import get_random_string


def pg_records(request, list, num):
    pass


def generate_activation_key(username):
    chars = "abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)"
    secret_key = get_random_string(20, chars)
    return hashlib.sha256((secret_key + username).encode("utf-8")).hexdigest()


def generate_otp():
    chars = "abcdefghijklmnopqrstuvwxyz0123456789"
    return get_random_string(6, chars)
