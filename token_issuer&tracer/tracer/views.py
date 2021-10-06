from django.db.models import base
from django.shortcuts import render, get_object_or_404
from django import forms
from tracer import models
from .models import Identity, Closecontact
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.
def index(request):
    return render(request, 'tracer/tracer.html')
    
def close_contact(request):
    if request.method == 'POST':
        positive_id=request.POST.get('pos_id', None)
        close_contact_instances = Closecontact.objects.filter(positivecase_id=positive_id)
        num_contact=close_contact_instances.count()
        if not close_contact_instances:
            return render(request, 'tracer/tracer_error_message.html', {'message':"Invalid postive case id! Make sure you enter the right number."})

        contact_list = Closecontact.objects.filter(positivecase_id=positive_id)
        template = loader.get_template('tracer/contacts_info.html')
        contact_list_dict={}
        for contact in contact_list:
            identity=Identity.objects.get(id=contact.identity_id)
            name = identity.fullname
            nric = identity.nric
            phone_num = identity.phone_num
            address = identity.address
            contact_list_dict[contact]={'name': name, 'nric': nric, 
                                'phone_num': phone_num, 'address': address}
        context = {
            'contact_list_dict': contact_list_dict,
        }

        return HttpResponse(template.render(context, request))
    return render(request, 'tracer/close_contact.html')   
        
        #check whether the nric is in the database or not
        
        
#        identity_info={}
#        info=json.loads(json.dumps(identity_info))
#        for i in range(0, num_contact):
#            identity_instance = models.Identity.objects.filter(id=close_contact_instances[i].identity_id).first()
#            identity_info={'nric': identity_instance.nric, 
#                            'fullname': identity_instance.fullname, 
#                            'phone_num': identity_instance.phone_num, 
#                            'address': identity_instance.address}
#           info["contact %d" % i] = identity_info
#        contacts_info = json.dumps(info)
#        return render(request, 'contacts_info.html', {'info': contacts_info})

#    

def contacts_info(context, request):
    template = loader.get_template('tracer/contacts_info.html')
    return HttpResponse(template.render(context, request))

def tracer_error_message(request, message):
    return render(request, 'tracer/tracer_error_message.html', {'message': message})

def find_contact(request):
    if request.method == 'POST':
        nric_num=request.POST.get('nric', None)
        identity_instance = Identity.objects.filter(nric=nric_num)
        if not identity_instance:
            return render(request, 'tracer/tracer_error_message.html', {'message': "The nric number is not recorded! Make sure all the credentials are correct."})
        else:
            identity = identity_instance[0].id
        
        identity = Identity.objects.filter(nric=nric_num)[0]
        contacts = Closecontact.objects.filter(identity_id=identity.id)
        if not contacts:
            return render(request, 'tracer/tracer_error_message.html', {'message': "The nric holder is not a close contact. You are not allowed to view the information"})

        template = loader.get_template('tracer/individual_info.html')
        contact_list_dict={}
        positive_id_arr=[]

        name = identity.fullname
        nric = identity.nric
        phone_num = identity.phone_num
        address = identity.address
        for case in contacts:
            positive_id_arr.append(case.positivecase_id)

        contact_list_dict[0]={'name': name, 'nric': nric, 
                            'phone_num': phone_num, 'address': address, 'positive_id_arr': positive_id_arr}
        context = {

            'contact_list_dict': contact_list_dict,
        }

        return HttpResponse(template.render(context, request))
    return render(request, 'tracer/find_contact.html')

def individual_info(context, request):
    template = loader.get_template('tracer/individual_info.html')
    return HttpResponse(template.render(context, request))
