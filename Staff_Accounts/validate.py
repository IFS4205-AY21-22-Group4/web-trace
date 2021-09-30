from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import Group
from django.core.mail import send_mail


def validateRoles(form, role):
    group_error = False
    if role.lower() == "administrators":
        user = form.save()  # Should only be saved if groups are valid
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
        group_error = True
    return group_error


def validateEmail(request, activation_key):
    email_verification_error = False

    subject = "Central Login Account Verification"

    message = """\n
            Please visit the following link to verify your account \n\n{0}://{1}/activate/account/?key={2}
                                    """.format(
        request.scheme, request.get_host(), activation_key
    )

    try:
        send_mail(subject, message, settings.SERVER_EMAIL, [request.POST["email"]])
    except:
        email_verification_error = True
    return email_verification_error


def validateOTP(request, current_otp, user):
    email_otp_error = False

    subject = "Central Login OTP"

    message = (
        """\n
            This is your current OTP:
                                    """
        + current_otp
    )

    print(user.email)
    try:
        send_mail(subject, message, settings.SERVER_EMAIL, [user.email])
    except:
        email_otp_error = True
    return email_otp_error
