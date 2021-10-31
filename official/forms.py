from django import forms
from .models import Staff, Cluster


class InsertForm(forms.Form):
    nric = forms.CharField(
        max_length=9,
        label="NRIC",
        error_messages={"required": "The identity id is required."},
    )
    date_test_positive = forms.DateField(
        widget=forms.widgets.DateInput(attrs={"type": "date"})
    )
    is_recovered = forms.BooleanField(
        label="The positive case has recovered", required=False
    )
    staff = forms.ModelChoiceField(
        label="Staff assigned",
        queryset=Staff.objects.filter(user__groups__name="Contact Tracers"),
        required=False,
    )
    cluster = forms.ModelChoiceField(
        label="Cluster", queryset=Cluster.objects.filter(status=True), required=True
    )


class UpdateForm(forms.Form):
    nric = forms.CharField(max_length=9, label="NRIC")


class EditForm(forms.Form):
    date_test_positive = forms.DateField(
        widget=forms.widgets.DateInput(attrs={"type": "date"}), required=False
    )
    is_recovered = forms.BooleanField(
        label="The positive case has recovered", required=False
    )
    staff = forms.ModelChoiceField(
        label="Staff assigned",
        queryset=Staff.objects.filter(user__groups__name="Contact Tracers"),
        required=False,
    )
    cluster = forms.ModelChoiceField(
        label="Cluster", queryset=Cluster.objects.filter(status=True), required=False
    )


class ConfirmForm(forms.Form):
    date_test_positive_change = forms.BooleanField(label="change", required=False)
    is_recovered_change = forms.BooleanField(label="change", required=False)
    staff_change = forms.BooleanField(label="change", required=False)
    cluster_change = forms.BooleanField(label="change", required=False)


class AssignForm(forms.Form):
    cluster = forms.ModelChoiceField(
        label="Cluster", queryset=Cluster.objects.filter(status=True), required=True
    )
    staff = forms.ModelChoiceField(
        label="Staff assigned",
        queryset=Staff.objects.filter(user__groups__name="Contact Tracers"),
        required=True,
    )


class AddForm(forms.Form):
    name = forms.CharField(max_length=10)
