from django import forms
from .models import Staff, Cluster

class InsertForm(forms.Form):
    identity_id = forms.DecimalField(label='Identity ID', error_messages={'required': 'The identity id is required.'})
    date_test_positive = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    is_recovered = forms.BooleanField(label='The positive case has recovered', required=False)
    staff = forms.ModelChoiceField(label='Staff assigned', queryset=Staff.objects.all(), required=False)
    # have_cluster = forms.BooleanField(label='The positive case belongs to an existing cluster')
    cluster = forms.ModelChoiceField(label='Cluster', queryset=Cluster.objects.all(), required=False)
                                     # widget=forms.HiddenInput()

class UpdateForm(forms.Form):
    positivecase_id = forms.DecimalField(label='Positive case ID')
    date_test_positive = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    is_recovered = forms.BooleanField(label='The positive case has recovered', required=False)
    staff = forms.ModelChoiceField(label='Staff assigned', queryset=Staff.objects.all(), required=False)
    cluster = forms.ModelChoiceField(label='Cluster', queryset=Cluster.objects.all(), required=False)

class ConfirmForm(forms.Form):
    date_test_positive_change = forms.BooleanField(label='change', required=False)
    is_recovered_change = forms.BooleanField(label='change', required=False)
    staff_change = forms.BooleanField(label='change', required=False)
    cluster_change = forms.BooleanField(label='change', required=False)