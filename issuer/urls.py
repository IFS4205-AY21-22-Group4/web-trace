from django.urls import path

from . import views

app_name = "issuer"
urlpatterns = [
    path("", views.index, name="index"),
    path("issue_token/", views.issue_token, name="issue_token"),
    path("inactivate_token/", views.inactivate_token, name="inactivate_token"),
    path("error_message/", views.error_message, name="error_message"),
]
