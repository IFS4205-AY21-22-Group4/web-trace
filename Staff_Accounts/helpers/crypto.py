import hashlib, logging
from django.utils.crypto import get_random_string

from config.settings import DB

db_logger = logging.getLogger(DB)


def pg_records(request, list, num):
    pass


def generate_activation_key(email):
    db_logger.info("generate_activation_ley")
    chars = "abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)"
    secret_key = get_random_string(20, chars)
    return hashlib.sha256((secret_key + email).encode("utf-8")).hexdigest()


def generate_otp():
    db_logger.info("generate_otp")
    chars = "abcdefghijklmnopqrstuvwxyz0123456789"
    return get_random_string(6, chars)
