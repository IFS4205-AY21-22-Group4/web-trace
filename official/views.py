from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.template import loader
from .models import (
    Identity,
    PositiveCases,
    Staff,
    Cluster,
    CloseContact,
    Edge,
    Token,
    Gateway,
    GatewayRecord,
)

# from Staff_Accounts.models import Staff
from .forms import InsertForm, UpdateForm, ConfirmForm, EditForm
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from Staff_Accounts.helpers.wrappers import (
    admin_only,
    unauthenticated_user,
    unverified_user,
    verified_user,
)

# @verified_user
def index(request):
    cluster_list = Cluster.objects.filter(status=True).order_by("id")
    template = loader.get_template("official/index.html")
    cluster_number_dict = {}
    for cluster in cluster_list:
        cases_count = cluster.positivecases_set.filter(is_recovered=False).count()
        contacts_count = cluster.closecontact_set.all().count()
        cluster_number_dict[cluster] = {
            "cases_count": cases_count,
            "contacts_count": contacts_count,
        }
    context = {
        "cluster_number_dict": cluster_number_dict,
    }
    return HttpResponse(template.render(context, request))


# @verified_user
def detail(request, cluster_id):
    cluster = get_object_or_404(Cluster, pk=cluster_id)
    cases = cluster.positivecases_set.filter(is_recovered=False)
    contacts = cluster.closecontact_set.all()
    links = cluster.edge_set.all()
    template = loader.get_template("official/detail.html")
    context = {
        "cluster": cluster,
        "cases": cases,
        "contacts": contacts,
        "links": links,
    }
    # return render(request, 'official/detail.html', {'cluster': cluster})
    return HttpResponse(template.render(context, request))


# @verified_user
@csrf_protect
def insert(request):
    staffs = list(Staff.objects.filter(roles="contact tracers"))
    clusters = Cluster.objects.filter(status=True)
    case_num = PositiveCases.objects.count() + 1
    template = loader.get_template("official/insert.html")
    if request.method == "POST":
        form = InsertForm(request.POST)
        try:
            if form.is_valid():
                nric = form.cleaned_data["nric"]
                try:
                    identity = Identity.objects.get(nric=nric)
                except:
                    return HttpResponseRedirect(
                        reverse("official:error", args=("NRIC does not exist.",))
                    )
                date_test_positive = form.cleaned_data["date_test_positive"]
                is_recovered = form.cleaned_data["is_recovered"]
                staff = form.cleaned_data["staff"]
                cluster = form.cleaned_data["cluster"]
                if cluster:
                    case = PositiveCases(
                        identity=identity,
                        date_test_positive=date_test_positive,
                        is_recovered=is_recovered,
                        staff=staff,
                        cluster=cluster,
                    )
                else:
                    case = PositiveCases(
                        identity=identity,
                        date_test_positive=date_test_positive,
                        is_recovered=is_recovered,
                        staff=staff,
                    )
                case.save()
                # messages.success(request, "Your data has been saved!")
                return HttpResponseRedirect(reverse("official:success"))
        except Exception as e:
            return HttpResponseRedirect(reverse("official:error", args=(e,)))

    else:
        form = InsertForm()
    context = {
        "staffs": staffs,
        "clusters": clusters,
        "case_num": case_num,
        "form": form,
    }
    return HttpResponse(template.render(context, request))


# @verified_user
@csrf_protect
def update(request):
    template = loader.get_template("official/update.html")
    information = None
    if request.method == "POST":
        form = UpdateForm(request.POST)
        if form.is_valid():
            nric = form.cleaned_data["nric"]
            return HttpResponseRedirect(reverse("official:confirm", args=(nric,)))
    else:
        form = UpdateForm()
    context = {
        "form": form,
    }
    return HttpResponse(template.render(context, request))


# @verified_user
def confirm(request, nric):
    template = loader.get_template("official/confirm.html")
    case = PositiveCases.objects.get(nric=nric)
    if request.method == "POST":
        form = ConfirmForm(request.POST)
        if form.is_valid():
            date_test_positive_change = form.cleaned_data["date_test_positive_change"]
            is_recovered_change = form.cleaned_data["is_recovered_change"]
            staff_change = form.cleaned_data["staff_change"]
            cluster_change = form.cleaned_data["cluster_change"]
            change_dict = {
                "date_test_positive_change": date_test_positive_change,
                "is_recovered_change": is_recovered_change,
                "staff_change": staff_change,
                "cluster_change": cluster_change,
            }
            return HttpResponseRedirect(
                reverse("official:edit", args=(nric, change_dict))
            )
    else:
        form = ConfirmForm()
    context = {
        "form": form,
        "case": case,
        "positivecase_id": nric,
    }
    return HttpResponse(template.render(context, request))


# @verified_user
def edit(request, positivecase_id, change_dict):
    staffs = Staff.objects.all()
    clusters = Cluster.objects.all()
    template = loader.get_template("official/edit.html")
    if request.method == "POST":
        form = EditForm(request.POST)
    #     if form.is_valid():
    #         identity_id = form.cleaned_data["identity_id"]
    #         identity = Identity.objects.get(pk=identity_id)
    #         date_test_positive = form.cleaned_data["date_test_positive"]
    #         is_recovered = form.cleaned_data["is_recovered"]
    #         staff = form.cleaned_data["staff"]
    #         cluster = form.cleaned_data["cluster"]
    #         if cluster:
    #             case = PositiveCases(
    #                 identity=identity,
    #                 date_test_positive=date_test_positive,
    #                 is_recovered=is_recovered,
    #                 staff=staff,
    #                 cluster=cluster,
    #             )
    #         else:
    #             case = PositiveCases(
    #                 identity=identity,
    #                 date_test_positive=date_test_positive,
    #                 is_recovered=is_recovered,
    #                 staff=staff,
    #             )
    #         case.save()
    #         return HttpResponseRedirect(reverse("official:success"))
    # else:
    #     form = InsertForm()
    context = {
        "staffs": staffs,
        "clusters": clusters,
        # "form": form,
    }
    return HttpResponse(template.render(context, request))


# @verified_user
def assign(request):
    return HttpResponse(
        "Please assign a tracer to a positive case or close contact here."
    )


def success(request):
    template = loader.get_template("official/success.html")
    context = {}
    return HttpResponse(template.render(context, request))


def error(request, message):
    template = loader.get_template("official/error.html")
    context = {"message": message}
    return HttpResponse(template.render(context, request))
