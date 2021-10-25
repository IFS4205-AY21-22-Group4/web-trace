import hashlib, logging
from django.utils.crypto import get_random_string
from Staff_Accounts.models import Staff

from config.settings import DB, SECRET_KEY

db_logger = logging.getLogger(DB)


def pg_records(request, list, num):
    pass


def generate_activation_key(email):
    db_logger.info("generate_activation_ley")
    chars = "abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)"
    while True:
        saltPre = get_random_string(20, chars)
        saltPost = get_random_string(20, chars)
        activation_key = hashlib.sha512(
            (saltPre + SECRET_KEY + email + saltPost).encode("utf-8")
        ).hexdigest()
        try:
            new_session_user = Staff.objects.get(activation_key=activation_key)
        except:
            break
    return activation_key


def generate_otp():
    db_logger.info("generate_otp")
    chars = "abcdefghijklmnopqrstuvwxyz0123456789"
    return get_random_string(6, chars)
