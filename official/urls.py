from django.urls import path

from . import views

app_name = "official"
urlpatterns = [
    path("", views.index, name="index"),
    path("<int:cluster_id>/", views.detail, name="detail"),
    path("insert/", views.insert, name="insert"),
    path("update/", views.update, name="update"),
    path("assign/", views.assign, name="assign"),
    path("edit/<int:positivecase_id>/", views.edit, name="edit"),
    path("success/", views.success, name="success"),
    path("confirm/<int:positivecase_id>/", views.confirm, name="confirm"),
    path("error/<message>/", views.error, name="error"),
    path("showcontact/<int:positivecase_id>", views.showcontact, name="showcontact"),
    path("assign/", views.assign, name="assign"),
]
