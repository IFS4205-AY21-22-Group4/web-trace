from django.db.models import base
from django.shortcuts import render
from django.http import HttpResponse
from django import forms
from issue_token import models
import hashlib

# Create your views here.
def index(request):
    # return HttpResponse("You are at the token issuer interface.")
    return render(request, "issuer/index.html")


def issue_token(request):
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
        token_instance = models.Token.objects.filter(identity_id=identity).filter(
            status=1
        )
        if token_instance:
            # return HttpResponse("The nric holder still has an active token!")
            return render(
                request,
                "issuer/error.html",
                {
                    "message": "The nric holder still has an active token! Make sure all the credentials are correct."
                },
            )

        # check whether the user has medical records
        identity = (models.Identity.objects.get(nric=nric_num).id,)
        record = models.Medicalrecords.objects.filter(identity_id=identity)
        if not record:
            return render(
                request,
                "issuer/error.html",
                {
                    "message": "The nric holder does not have medical records! Contact the administrator for more information."
                },
            )
        record = record[0]

        new_token = models.Token.objects.create(
            token_serial_number=serial,
            identity=models.Identity.objects.get(nric=nric_num),
            staff_id=1,  # temporary all set to 1
            status=1,  # 1 for active
            hashed_pin=h_pin,
        )

        # update medical records table
        record.token = models.Token.objects.filter(token_serial_number=serial)[0]
        # record.token = new_token
        record.save()

    return render(request, "issuer/issue_token.html")


def inactivate_token(request):
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

        identity = (models.Identity.objects.get(nric=nric_num).id,)
        record = models.Medicalrecords.objects.filter(identity_id=identity)
        if not record:
            return render(
                request,
                "issuer/error.html",
                {
                    "message": "The nric holder does not have medical records! Contact the administrator for more information."
                },
            )
        record = record[0]

        token_instance = models.Token.objects.filter(identity_id=identity).filter(
            status=1
        )
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

    return render(request, "issuer/inactivate_token.html")


def inact_result(request):
    message = "You have inactivated a token successfully."
    return render(request, "issuer/inact_result.html", {"message": message})


def error_message(request, message):
    return render(request, "issuer/error_message.html", {"message": message})
