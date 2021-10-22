from django.db.models import base
from django.shortcuts import render
from django.http import HttpResponse
from django import forms
from issuer import models
import hashlib
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate, get_user_model, login, logout
from Staff_Accounts.models import Staff, User, UserManager


# Create your views here.
def index(request):
    # return HttpResponse("You are at the token issuer interface.")
    return render(request, "issuer/index.html")


@csrf_protect
def issue_token(request, message=""):
    if request.method == "POST":

        serial = request.POST.get("serial", None)
        nric_num = request.POST.get("nric", None)
        pin = request.POST.get("pin", None)
        if pin is not None:
            pin = pin.encode("utf-8")
            h_pin = hashlib.sha256(pin).hexdigest()
        else:
            h_pin = None

        # check whether the nric is in the database or not
        identity_instance = models.Identity.objects.filter(nric=nric_num)
        if not identity_instance:
            return render(
                request,
                "issuer/error.html",
                {
                    "message": "The nric number is not recorded! Make sure all the credentials are correct or contact the administrator."
                },
            )
        else:
            identity = identity_instance[0].id

        # check whether the user have active token
        token_instance = models.Token.objects.filter(owner_id=identity).filter(status=1)
        if token_instance:
            return render(
                request,
                "issuer/error.html",
                {
                    "message": "The nric holder still has an active token! Make sure all the credentials are correct."
                },
            )

        # check whether the token is on use
        active_token = models.Token.objects.filter(token_uuid=serial).filter(status=1)
        if active_token:
            return render(
                request,
                "issuer/error.html",
                {
                    "message": "The token is using by another user. Make sure the serial number of the token is correct."
                },
            )
        # check whether the user has medical records
        identity = (models.Identity.objects.get(nric=nric_num).id,)
        record = models.MedicalRecord.objects.filter(identity_id=identity)
        if not record:
            return render(
                request,
                "issuer/error.html",
                {
                    "message": "The nric holder does not have medical records! Contact the administrator for more information."
                },
            )
        record = record[0]

        # get staff
        user = request.user.id
        staff_instance = models.Staff.objects.filter(user_id=user)
        if not staff_instance:
            return render(
                request,
                "issuer/error.html",
                {"message": "The staff is not recorded."},
            )
        else:
            staff = identity_instance[0]

        new_token = models.Token.objects.create(
            token_uuid=serial,
            # identity=models.Identity.objects.get(nric=nric_num),
            owner=models.Identity.objects.get(nric=nric_num),
            # staff_id=1,  # temporary all set to 1
            # staff = get_user_model().objects.get(user=request.user).id,
            issuer=staff,
            status=1,  # 1 for active
            hashed_pin=h_pin,
        )

        # update medical records table
        # record.token = models.Token.objects.filter(token_serial_number=serial)[0]
        record.token = models.Token.objects.filter(token_uuid=serial)[0]
        # record.token = new_token
        record.save()
        message = "Token is issued successfully!"
        return render(request, "issuer/issue_token.html", {"message": message})
    else:
        return render(request, "issuer/issue_token.html")


@csrf_protect
def inactivate_token(request, message=""):
    # need to test
    if request.method == "POST":
        nric_num = request.POST.get("nric", None)
        identity_instance = models.Identity.objects.filter(nric=nric_num)
        if not identity_instance:
            return render(
                request,
                "issuer/error.html",
                {
                    "message": "The nric number is not recorded! Make sure all the credentials are correct."
                },
            )
        else:
            identity = identity_instance[0].id

        identity = models.Identity.objects.get(nric=nric_num).id
        record = models.MedicalRecord.objects.filter(identity_id=identity)
        if not record:
            return render(
                request,
                "issuer/error.html",
                {
                    "message": "The nric holder does not have medical records! Contact the administrator for more information."
                },
            )
        record = record[0]

        token_instance = models.Token.objects.filter(owner_id=identity).filter(status=1)
        if not token_instance:
            # return HttpResponse("The nric holder has no active token!")
            return render(
                request,
                "issuer/error.html",
                {"message": "The nric holder has no active token!"},
            )
        else:
            token_instance[0].status = 0
            token_instance[0].save()
            record.token = None
            record.save()
        message = "Token is inactivated successfully!"
        return render(request, "issuer/inactivate_token.html", {"message": message})
    else:
        return render(request, "issuer/inactivate_token.html")


# def inact_result(request):
#    message = "You have inactivated a token successfully."
#    return render(request, "issuer/inact_result.html", {"message": message})


def error_message(request, message):
    return render(request, "issuer/error_message.html", {"message": message})
