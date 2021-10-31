from django.db.models import base
from django.shortcuts import render, get_object_or_404
from django import forms

# from tracer import models
# from .models import Identity, CloseContact
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate, get_user_model, login, logout
from Staff_Accounts.models import Staff, User, UserManager
from issuer.models import Token, MedicalRecord, Identity
from Staff_Accounts.helpers.wrappers import tracer_only, verified_user
from official.models import Cluster, PositiveCases, CloseContact

# Create your views here.
@verified_user
@tracer_only
def index(request):
    return render(request, "tracer/tracer.html")


@csrf_protect
@verified_user
@tracer_only
def close_contact(request):
    template = loader.get_template("tracer/close_contact.html")
    case_list = []
    close_contacts = PositiveCases.objects.filter(staff_id=request.user.id)
    for instance in close_contacts:
        case_list.append(instance.id)

    if request.method == "POST":
        positive_id = request.POST.get("pos_id", None)
        close_contact_instances = CloseContact.objects.filter(
            positivecase_id=positive_id
        ).filter(status=1)
        num_contact = close_contact_instances.count()
        if not close_contact_instances:
            return render(
                request,
                "tracer/tracer_error_message.html",
                {
                    "message": "Invalid postive case id or there is no close contact of that positive case assigned to you."
                },
            )

        user = request.user.id
        contact_list = (
            CloseContact.objects.filter(positivecase_id=positive_id)
            .filter(staff_id=user)
            .filter(status=1)
        )
        template = loader.get_template("tracer/contacts_info.html")
        contact_list_dict = {}
        for contact in contact_list:
            identity = Identity.objects.get(id=contact.identity_id)
            nric = identity.nric
            contact_list_dict[contact] = {
                "nric": nric,
            }
        context = {
            "contact_list_dict": contact_list_dict,
        }

        return HttpResponse(template.render(context, request))

    return HttpResponse(template.render({"case_list": case_list}, request))


@verified_user
@tracer_only
def contacts_info(context, request):
    template = loader.get_template("tracer/contacts_info.html")
    return HttpResponse(template.render(context, request))


@verified_user
@tracer_only
def tracer_error_message(request, message):
    return render(request, "tracer/tracer_error_message.html", {"message": message})


@verified_user
@tracer_only
@csrf_protect
def find_contact(request):
    if request.method == "POST":
        nric_num = request.POST.get("nric", None)
        identity_instance = Identity.objects.filter(nric=nric_num)
        if not identity_instance:
            return render(
                request,
                "tracer/tracer_error_message.html",
                {
                    "message": "The nric number is not recorded! Make sure all the credentials are correct."
                },
            )
        else:
            identity = identity_instance[0].id

        identity = Identity.objects.filter(nric=nric_num)[0]
        user = request.user.id
        contacts = (
            CloseContact.objects.filter(identity_id=identity.id)
            .filter(staff_id=user)
            .filter(status=1)
        )
        if not contacts:
            return render(
                request,
                "tracer/tracer_error_message.html",
                {
                    "message": "You are not allowed to view the information of this NRIC holder or the holder is not a close contact."
                },
            )

        template = loader.get_template("tracer/individual_info.html")
        contact_list_dict = {}
        positive_id_arr = []

        name = identity.fullname
        nric = identity.nric
        phone_num = identity.phone_num
        address = identity.address
        for case in contacts:
            positive_id_arr.append(case.positivecase_id)

        contact_list_dict[0] = {
            "name": name,
            "nric": nric,
            "phone_num": phone_num,
            "address": address,
            "positive_id_arr": positive_id_arr,
        }
        context = {
            "contact_list_dict": contact_list_dict,
        }

        return HttpResponse(template.render(context, request))
    return render(request, "tracer/find_contact.html")


@verified_user
@tracer_only
def individual_info(context, request):
    template = loader.get_template("tracer/individual_info.html")
    return HttpResponse(template.render(context, request))


@verified_user
@tracer_only
def individual_detail(request, nric=""):
    template = loader.get_template("tracer/individual_info.html")
    nric_num = nric
    identity_instance = Identity.objects.filter(nric=nric_num)
    if not identity_instance:
        return render(
            request,
            "tracer/tracer_error_message.html",
            {
                "message": "The nric number is not recorded! Make sure all the credentials are correct."
            },
        )
    else:
        identity = identity_instance[0]

    contacts = (
        CloseContact.objects.filter(identity_id=identity.id)
        .filter(staff_id=request.user.id)
        .filter(status=1)
    )
    if not contacts:
        return render(
            request,
            "tracer/tracer_error_message.html",
            {
                "message": "You are not allowed to view the information of this NRIC holder or the holder is not a close contact."
            },
        )

    contact_list_dict = {}
    positive_id_arr = []

    name = identity.fullname
    phone_num = identity.phone_num
    address = identity.address
    for case in contacts:
        positive_id_arr.append(case.positivecase_id)

    contact_list_dict[0] = {
        "name": name,
        "nric": nric_num,
        "phone_num": phone_num,
        "address": address,
        "positive_id_arr": positive_id_arr,
    }
    context = {
        "contact_list_dict": contact_list_dict,
    }
    return HttpResponse(template.render(context, request))


@verified_user
@tracer_only
@csrf_protect
def inactivate_contact(request, message=""):
    if request.method == "POST":
        nric_num = request.POST.get("nric", None)
        identity_instance = Identity.objects.filter(nric=nric_num)
        if not identity_instance:
            return render(
                request,
                "tracer/tracer_error_message.html",
                {
                    "message": "The nric number is not recorded! Make sure all the credentials are correct."
                },
            )
        identity = identity_instance[0].id

        contacts = (
            CloseContact.objects.filter(identity_id=identity)
            .filter(staff_id=request.user.id)
            .filter(status=1)
        )
        if not contacts:
            return render(
                request,
                "tracer/tracer_error_message.html",
                {
                    "message": "You are not allowed to inactivate this NRIC holder or the holder is not an activate close contact."
                },
            )
        else:
            for contact in contacts:
                contact.status = 0
                contact.save()
        message = "You have insctivated this close contacts successfully!"
        return render(request, "tracer/inactivate_contact.html", {"message": message})
    else:
        return render(request, "tracer/inactivate_contact.html")
