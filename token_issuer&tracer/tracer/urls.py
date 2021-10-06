from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='tracer'),
    path('close_contact/', views.close_contact, name='close_contact'),
    path('contacts_info/', views.contacts_info, name='contacts_info'),
    path('find_contact/', views.find_contact, name='find_contact'),
    path('individual_info/', views.individual_info, name='individual_info'),
    #path('modify_role/', views.modify_role, name='modify_role'),
    path('tracer_error/', views.tracer_error_message, name="tracer_error_message"),
]
