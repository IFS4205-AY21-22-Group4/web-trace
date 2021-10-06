from django.urls import path

from . import views

app_name = "official"
urlpatterns = [
    path("", views.index, name="index"),
    path("<int:cluster_id>/", views.detail, name="detail"),
    path("insert/", views.insert, name="insert"),
    path("update/", views.update, name="update"),
    path("assign/", views.assign, name="assign"),
    path("<int:positivecase_id>/edit/", views.edit, name="edit"),
    path("success/", views.success, name="success"),
    path("confirm/<int:positivecase_id>/", views.confirm, name="confirm"),
]
