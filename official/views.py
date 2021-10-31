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
import logging
from config.settings import DB

from .forms import InsertForm, UpdateForm, ConfirmForm, EditForm, AssignForm, AddForm
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from Staff_Accounts.helpers.wrappers import (
    admin_only,
    unauthenticated_user,
    unverified_user,
    verified_user,
    official_only,
)

db_logger = logging.getLogger(DB)


@verified_user
@official_only
def index(request):
    try:
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
        cases_no_cluster = PositiveCases.objects.filter(cluster=None)
        context = {
            "cluster_number_dict": cluster_number_dict,
            "cases_no_cluster": cases_no_cluster,
        }
        # db_logger.info("Official Index Page")
    except Exception as e:
        return HttpResponseRedirect(reverse("official:error", args=(e,)))
    return HttpResponse(template.render(context, request))


@verified_user
@official_only
def detail(request, cluster_id):
    try:
        cluster = get_object_or_404(Cluster, pk=cluster_id)
        cases = cluster.positivecases_set.filter(is_recovered=False)
        contacts = cluster.closecontact_set.filter(status=True)
        links = set()
        for edge in list(cluster.edge_set.all().distinct()):
            if (
                edge.vertex1_category == "positive"
                and edge.vertex2_category == "positive"
            ):
                if (
                    PositiveCases.objects.get(id=edge.vertex1_id).is_recovered == False
                    and PositiveCases.objects.get(id=edge.vertex2_id).is_recovered
                    == False
                ):
                    links.add(
                        (
                            "positive",
                            "positive",
                            PositiveCases.objects.get(id=edge.vertex1_id),
                            PositiveCases.objects.get(id=edge.vertex2_id),
                        )
                    )
            elif (
                edge.vertex1_category == "positive"
                and edge.vertex2_category == "contact"
            ):
                if (
                    PositiveCases.objects.get(id=edge.vertex1_id).is_recovered == False
                    and CloseContact.objects.get(id=edge.vertex2_id).status == True
                ):
                    links.add(
                        (
                            "positive",
                            "contact",
                            PositiveCases.objects.get(id=edge.vertex1_id),
                            CloseContact.objects.get(id=edge.vertex2_id),
                        )
                    )
            elif (
                edge.vertex1_category == "contact"
                and edge.vertex2_category == "positive"
            ):
                if (
                    CloseContact.objects.get(id=edge.vertex1_id).status == True
                    and PositiveCases.objects.get(id=edge.vertex2_id).is_recovered
                    == False
                ):
                    links.add(
                        (
                            "contact",
                            "positive",
                            CloseContact.objects.get(id=edge.vertex1_id),
                            PositiveCases.objects.get(id=edge.vertex2_id),
                        )
                    )

        template = loader.get_template("official/detail.html")
        context = {
            "cluster": cluster,
            "cases": cases,
            "contacts": contacts,
            "links": links,
        }
        # db_logger.info("Official Detail Page of Cluster " + str(cluster_id))
    except Exception as e:
        return HttpResponseRedirect(reverse("official:error", args=(e,)))
    return HttpResponse(template.render(context, request))


@verified_user
@official_only
@csrf_protect
def insert(request):
    try:
        staffs = list(Staff.objects.filter(user__groups__name="Contact Tracers"))
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
                                "official:error",
                                args=("Date test positive is not valid.",),
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
                    all_current_nric = [
                        identity.nric for identity in all_current_identity
                    ]
                    if nric in all_current_nric:
                        return HttpResponseRedirect(
                            reverse(
                                "official:error",
                                args=("The positive case has already existed.",),
                            )
                        )

                    if cluster:
                        case = PositiveCases(
                            id=case_num,
                            identity=identity,
                            date_test_positive=date_test_positive,
                            is_recovered=is_recovered,
                            staff=staff,
                            cluster=cluster,
                        )
                    else:
                        case = PositiveCases(
                            id=case_num,
                            identity=identity,
                            date_test_positive=date_test_positive,
                            is_recovered=is_recovered,
                            staff=staff,
                        )

                    case.save()

                    # if staff:
                    #     staff_str = ", staff = " + str(staff.pk)
                    # else:
                    #     staff_str = ""
                    # if cluster:
                    #     cluster_str = ", cluster = " + str(cluster.id)
                    # else:
                    #     cluster_str = ""

                    # db_logger.info("Official Insert Page: Add PositiveCases: id = " + str(case_num) + ", identity = "
                    #                + str(identity.pk) + ", date_test_positive = " + str(date_test_positive)
                    #                + ", is_recovered = " + str(is_recovered) + staff_str + cluster_str + ".")

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
                        q3 = Q(gateway=gateway_record.gateway)

                        tokens_id_found = list(
                            GatewayRecord.objects.filter(q1 & q2 & q3).values_list(
                                "token", flat=True
                            )
                        )
                        tokens_found.extend(
                            list(Token.objects.filter(pk__in=tokens_id_found))
                        )

                    existing_identity_ids = list(
                        case.closecontact_set.all().values_list("identity", flat=True)
                    )

                    existing_pair = [
                        set(
                            [
                                str(edge.vertex1_category) + str(edge.vertex1_id),
                                str(edge.vertex2_category) + str(edge.vertex2_id),
                            ]
                        )
                        for edge in Edge.objects.all()
                    ]

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
                        if close_contact.identity != case.identity:
                            close_contact.save()
                            # db_logger.info("Official Insert Page: Add CloseContact: " + "id = " + str(idx) + ", identity = "
                            #                + str(identity_found.pk) + ", positivecase = " + str(case.id) + ", staff = "
                            #                + str(case.staff) + ", cluster = " + str(case.cluster.id))
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
                            pair = set(
                                [
                                    str(edge.vertex1_category) + str(edge.vertex1_id),
                                    str(edge.vertex2_category) + str(edge.vertex2_id),
                                ]
                            )
                            if pair not in existing_pair:
                                edge.save()
                                # db_logger.info("Official Insert Page: Add Edge: id = " + str(id) + ", vertex1_id = " + str(close_contact.id)
                                #              + ", vertex1_category = contact, vertex2_id = " + str(case.id)
                                #              + ", vertex2_category = positive, cluster = " + str(case.cluster.id))
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
        # db_logger.info("Official Insert Page")
    except Exception as e:
        return HttpResponseRedirect(reverse("official:error", args=(e,)))
    return HttpResponse(template.render(context, request))


@verified_user
@official_only
@csrf_protect
def update(request):
    try:
        template = loader.get_template("official/update.html")
        if request.method == "POST":
            form = UpdateForm(request.POST)
            if form.is_valid():
                nric = form.cleaned_data["nric"]
                case = PositiveCases.objects.filter(identity__nric=nric).last()
                if not case:
                    return HttpResponseRedirect(
                        reverse(
                            "official:error", args=("Positive case does not exist.",)
                        )
                    )
                return HttpResponseRedirect(
                    reverse("official:confirm", args=(case.id,))
                )
        else:
            form = UpdateForm()
        context = {
            "form": form,
        }
        # db_logger.info("Official Update Page")
    except Exception as e:
        return HttpResponseRedirect(reverse("official:error", args=(e,)))
    return HttpResponse(template.render(context, request))


@verified_user
@official_only
@csrf_protect
def confirm(request, positivecase_id):
    try:
        template = loader.get_template("official/confirm.html")
        case = PositiveCases.objects.get(id=positivecase_id)
        if request.method == "POST":
            form = ConfirmForm(request.POST)
            if form.is_valid():
                date_test_positive_change = form.cleaned_data[
                    "date_test_positive_change"
                ]
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
        # db_logger.info("Official Confirm Page of PositiveCases " + str(positivecase_id))
    except Exception as e:
        return HttpResponseRedirect(reverse("official:error", args=(e,)))
    return HttpResponse(template.render(context, request))


@verified_user
@official_only
@csrf_protect
def edit(request, positivecase_id):
    try:
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
                                "official:error",
                                args=("Date test positive is not valid.",),
                            )
                        )
                    if not date_test_positive:
                        return HttpResponseRedirect(
                            reverse("official:error", args=("Please select a date.",))
                        )
                    case.date_test_positive = date_test_positive
                if change_dict["is_recovered_change"]:
                    is_recovered = form.cleaned_data["is_recovered"]
                    case.is_recovered = is_recovered
                if change_dict["staff_change"]:
                    staff = form.cleaned_data["staff"]
                    case.staff = staff
                if change_dict["cluster_change"]:
                    cluster = form.cleaned_data["cluster"]
                    if not cluster:
                        return HttpResponseRedirect(
                            reverse(
                                "official:error", args=("Please select a cluster.",)
                            )
                        )
                    case.cluster = cluster
                    close_contacts = case.closecontact_set.all()
                    for contact in close_contacts:
                        contact.cluster = cluster
                        contact.save()
                case.save()
                # db_logger.info("Official Edit Page: Edit PositiveCases: id = " + str(case.id) + ", identity = "
                #                + str(identity.pk) + ", date_test_positive = " + str(date_test_positive)
                #                + ", is_recovered = " + str(is_recovered) + ", staff = " + str(staff.pk) + ".")
                return HttpResponseRedirect(reverse("official:success"))
        else:
            form = EditForm()
        context = {
            "form": form,
            "change_dict": change_dict,
            "positivecase_id": positivecase_id,
            "case": case,
        }
        # db_logger.info("Official Edit Page of Positivecases " + str(case.id))
    except Exception as e:
        return HttpResponseRedirect(reverse("official:error", args=(e,)))
    return HttpResponse(template.render(context, request))


@verified_user
@official_only
@csrf_protect
def assign(request):
    try:
        template = loader.get_template("official/assign.html")
        if request.method == "POST":
            form = AssignForm(request.POST)
            if form.is_valid():
                cluster = form.cleaned_data["cluster"]
                staff = form.cleaned_data["staff"]
                if not cluster:
                    return HttpResponseRedirect(
                        reverse("official:error", args=("Cluster cannot be empty.",))
                    )
                if not staff:
                    return HttpResponseRedirect(
                        reverse(
                            "official:error", args=("Staff assigned cannot be empty.",)
                        )
                    )
                positive_cases = list(PositiveCases.objects.filter(cluster=cluster))
                close_contacts = list(CloseContact.objects.filter(cluster=cluster))
                for case in positive_cases:
                    case.staff = staff
                    case.save()
                    # db_logger.info("Official Assign Page: Edit PositiveCases: id = " + str(case.id) + ", identity = "
                    #            + str(case.identity.pk) + ", date_test_positive = " + str(case.date_test_positive)
                    #            + ", is_recovered = " + str(case.is_recovered) + ", staff = " + str(case.staff.pk) + ".")
                for contact in close_contacts:
                    contact.staff = staff
                    contact.save()
                return HttpResponseRedirect(reverse("official:success"))
        else:
            form = AssignForm()
        context = {
            "form": form,
        }
        # db_logger.info("Official Assign Page")
    except Exception as e:
        return HttpResponseRedirect(reverse("official:error", args=(e,)))
    return HttpResponse(template.render(context, request))


@verified_user
@official_only
@csrf_protect
def add(request):
    try:
        template = loader.get_template("official/add.html")
        cluster_num = Cluster.objects.count() + 1
        names = list(Cluster.objects.values_list("name", flat=True))
        if request.method == "POST":
            form = AddForm(request.POST)
            if form.is_valid():
                name = form.cleaned_data["name"]
                if name in names:
                    return HttpResponseRedirect(
                        reverse(
                            "official:error", args=("The name has already been used.",)
                        )
                    )
                cluster = Cluster(
                    id=cluster_num,
                    name=name,
                    status=True,
                )
                cluster.save()
                return HttpResponseRedirect(reverse("official:success"))
        else:
            form = AddForm()
        context = {
            "form": form,
            "cluster_num": cluster_num,
        }
    except Exception as e:
        return HttpResponseRedirect(reverse("official:error", args=(e,)))
    return HttpResponse(template.render(context, request))


@verified_user
@official_only
def success(request):
    try:
        template = loader.get_template("official/success.html")
        context = {}
    except Exception as e:
        return HttpResponseRedirect(reverse("official:error", args=(e,)))
    return HttpResponse(template.render(context, request))


@verified_user
@official_only
def showcontact(request, positivecase_id):
    try:
        template = loader.get_template("official/showcontact.html")
        close_contacts_id = request.session["close_contacts_id" + str(positivecase_id)]
        close_contacts = list(CloseContact.objects.filter(id__in=close_contacts_id))
        context = {
            "close_contacts": close_contacts,
            "positivecase": PositiveCases.objects.get(id=positivecase_id),
        }
    except Exception as e:
        return HttpResponseRedirect(reverse("official:error", args=(e,)))
    return HttpResponse(template.render(context, request))


@verified_user
@official_only
def error(request, message):
    template = loader.get_template("official/error.html")
    context = {"message": message}
    return HttpResponse(template.render(context, request))
