from django.shortcuts import render

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
import datetime
from django.db.models import Q

from .forms import InsertForm, UpdateForm, ConfirmForm, EditForm, AssignForm
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from Staff_Accounts.helpers.wrappers import (
    admin_only,
    unauthenticated_user,
    unverified_user,
    verified_user,
    official_only,
)


@verified_user
@official_only
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


@verified_user
@official_only
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


@verified_user
@official_only
@csrf_protect
def insert(request):
    staffs = list(Staff.objects.filter(user__groups__name="Contact Tracers"))
    # print(request.user.email)
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
                if date_test_positive > datetime.date.today():
                    return HttpResponseRedirect(
                        reverse(
                            "official:error", args=("Date test positive is not valid.",)
                        )
                    )
                is_recovered = form.cleaned_data["is_recovered"]
                staff = form.cleaned_data["staff"]
                cluster = form.cleaned_data["cluster"]

                all_current_identity_id = list(
                    PositiveCases.objects.filter(is_recovered=False).values_list(
                        "identity", flat=True
                    )
                )
                all_current_identity = list(
                    Identity.objects.filter(pk__in=all_current_identity_id)
                )
                all_current_nric = [identity.nric for identity in all_current_identity]
                # if nric in all_current_nric:
                #     return HttpResponseRedirect(
                #         reverse("official:error", args=("The positive case has already existed.",))
                #     )

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

                token = (
                    Token.objects.filter(owner=case.identity)
                    .filter(status=True)
                    .first()
                )
                gateway_records = list(GatewayRecord.objects.filter(token=token))
                tokens_found = list()
                idx = CloseContact.objects.all().count() + 1
                idx_edge = Edge.objects.all().count() + 1
                close_contacts = list()

                for gateway_record in gateway_records:
                    q1 = Q(
                        timestamp__lte=gateway_record.timestamp
                        + datetime.timedelta(0, 10800)
                    )
                    q2 = Q(
                        timestamp__gte=gateway_record.timestamp
                        - datetime.timedelta(0, 10800)
                    )

                    tokens_id_found = list(
                        GatewayRecord.objects.filter(q1 & q2).values_list(
                            "token", flat=True
                        )
                    )
                    tokens_found.extend(
                        list(Token.objects.filter(pk__in=tokens_id_found))
                    )

                existing_identity_ids = list(
                    case.closecontact_set.all().values_list("identity", flat=True)
                )
                for token in set(tokens_found):
                    identity_found = token.owner
                    if identity_found.pk in existing_identity_ids:
                        continue
                    close_contact = CloseContact(
                        id=idx,
                        identity=identity_found,
                        positivecase=case,
                        staff=case.staff,
                        cluster=case.cluster,
                    )
                    close_contact.save()
                    idx += 1
                    existing_identity_ids.append(identity_found.pk)
                    edge = Edge(
                        id=idx_edge,
                        vertex1_id=close_contact.id,
                        vertex1_category="contact",
                        vertex2_id=case.id,
                        vertex2_category="positive",
                        cluster=case.cluster,
                    )
                    edge.save()
                    idx_edge += 1
                    close_contacts.append(close_contact)

                request.session["close_contacts_id" + str(case.id)] = [
                    contact.id for contact in close_contacts
                ]

                return HttpResponseRedirect(
                    reverse("official:showcontact", args=(case.id,))
                )

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


@verified_user
@official_only
@csrf_protect
def update(request):
    template = loader.get_template("official/update.html")
    if request.method == "POST":
        form = UpdateForm(request.POST)
        if form.is_valid():
            nric = form.cleaned_data["nric"]
            case = (
                PositiveCases.objects.filter(identity__nric=nric)
                .filter(is_recovered=False)
                .last()
            )
            return HttpResponseRedirect(reverse("official:confirm", args=(case.id,)))
    else:
        form = UpdateForm()
    context = {
        "form": form,
    }
    return HttpResponse(template.render(context, request))


@verified_user
@official_only
@csrf_protect
def confirm(request, positivecase_id):
    template = loader.get_template("official/confirm.html")
    case = PositiveCases.objects.get(id=positivecase_id)
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
            request.session["change_dict" + str(positivecase_id)] = change_dict
            return HttpResponseRedirect(
                reverse("official:edit", args=(positivecase_id,))
            )
    else:
        form = ConfirmForm()
    context = {
        "form": form,
        "case": case,
        "positivecase_id": positivecase_id,
    }
    return HttpResponse(template.render(context, request))


@verified_user
@official_only
@csrf_protect
def edit(request, positivecase_id):
    staffs = Staff.objects.all()
    clusters = Cluster.objects.filter(status=True)
    template = loader.get_template("official/edit.html")
    change_dict = request.session["change_dict" + str(positivecase_id)]
    case = PositiveCases.objects.get(id=positivecase_id)
    if request.method == "POST":
        form = EditForm(request.POST)
        if form.is_valid():
            identity = case.identity
            date_test_positive = case.date_test_positive
            is_recovered = case.is_recovered
            staff = case.staff
            cluster = case.cluster
            if change_dict["date_test_positive_change"]:
                date_test_positive = form.cleaned_data["date_test_positive"]
                if date_test_positive > datetime.date.today():
                    return HttpResponseRedirect(
                        reverse(
                            "official:error", args=("Date test positive is not valid.",)
                        )
                    )
            if change_dict["is_recovered_change"]:
                is_recovered = form.cleaned_data["is_recovered"]
            if change_dict["staff_change"]:
                staff = form.cleaned_data["staff"]
            if change_dict["cluster_change"]:
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
            return HttpResponseRedirect(reverse("official:success"))
    else:
        form = EditForm()
    context = {
        "form": form,
        "change_dict": change_dict,
        "positivecase_id": positivecase_id,
        "case": case,
    }
    return HttpResponse(template.render(context, request))


@verified_user
@official_only
@csrf_protect
def assign(request):
    template = loader.get_template("official/assign.html")
    if request.method == "POST":
        form = AssignForm(request.POST)
        if form.is_valid():
            cluster = form.cleaned_data["cluster"]
            staff = form.cleaned_data["staff"]
            positive_cases = list(PositiveCases.objects.filter(cluster=cluster))
            close_contacts = list(CloseContact.objects.filter(cluster=cluster))
            for case in positive_cases:
                case.staff = staff
                case.save()
            for contact in close_contacts:
                contact.staff = staff
                contact.save()
            return HttpResponseRedirect(reverse("official:success"))
    else:
        form = AssignForm()
    context = {
        "form": form,
    }
    return HttpResponse(template.render(context, request))


@verified_user
@official_only
def success(request):
    template = loader.get_template("official/success.html")
    context = {}
    return HttpResponse(template.render(context, request))


@verified_user
@official_only
def showcontact(request, positivecase_id):
    template = loader.get_template("official/showcontact.html")
    close_contacts_id = request.session["close_contacts_id" + str(positivecase_id)]
    close_contacts = list(CloseContact.objects.filter(id__in=close_contacts_id))
    context = {
        "close_contacts": close_contacts,
        "positivecase": PositiveCases.objects.get(id=positivecase_id),
    }
    return HttpResponse(template.render(context, request))


@verified_user
@official_only
def error(request, message):
    template = loader.get_template("official/error.html")
    context = {"message": message}
    return HttpResponse(template.render(context, request))
